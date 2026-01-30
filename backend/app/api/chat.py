"""
Chat API Endpoints
Main chat endpoint for the legal triage agent.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

from app.api.auth import get_current_user
from app.agent.graph import create_agent_graph, run_agent
from app.agent.state import create_initial_state
from app.memory.long_term import save_message, get_session_messages
from app.db.supabase import get_supabase_client, get_service_client
from app.config import settings
from app.utils.logger import logger


router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request schema."""
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[str] = None
    llm_provider: Optional[str] = Field(default=None)


class SourceDocument(BaseModel):
    """Source document reference schema."""
    title: str
    section: str
    content: str
    source_url: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str
    session_id: str
    classification: Optional[str] = None
    sub_classification: Optional[str] = None
    confidence: float
    needs_clarification: bool
    sources: List[SourceDocument] = []
    disclaimer: str = (
        "This is procedural guidance only, not legal advice. "
        "Please consult a qualified legal professional for specific advice."
    )


class SessionCreateRequest(BaseModel):
    """Session creation request schema."""
    title: Optional[str] = None


class SessionResponse(BaseModel):
    """Session response schema."""
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, user: dict = Depends(get_current_user)):
    """
    Main chat endpoint.
    Processes user message through the legal triage agent.
    """
    try:
        # Get or create session
        session_id = request.session_id
        if not session_id:
            session_id = await create_new_session(user["id"])
        
        # Validate session belongs to user
        await validate_session_ownership(session_id, user["id"])
        
        # Get chat history for context
        chat_history = await get_session_messages(
            session_id, 
            limit=settings.max_context_messages
        )
        
        # Create initial agent state
        state = create_initial_state(
            user_input=request.message,
            session_id=session_id,
            user_id=user["id"],
            chat_history=chat_history
        )
        
        # Determine LLM provider
        llm_provider = request.llm_provider or settings.llm_provider
        
        # Run agent graph
        result = await run_agent(state, llm_provider)
        
        # Save messages to memory
        await save_message(
            session_id=session_id,
            role="user",
            content=request.message
        )
        await save_message(
            session_id=session_id,
            role="assistant",
            content=result["response"],
            metadata={
                "classification": result.get("classification"),
                "confidence": result.get("confidence")
            }
        )
        
        # Update session timestamp
        await update_session_timestamp(session_id)
        
        # Format source documents
        sources = []
        for doc in result.get("retrieved_docs", []):
            sources.append(SourceDocument(
                title=doc.get("title", "Legal Document"),
                section=doc.get("section", ""),
                content=doc.get("content", "")[:500],
                source_url=doc.get("source_url")
            ))
        
        return ChatResponse(
            response=result["response"],
            session_id=session_id,
            classification=result.get("classification", {}).get("domain"),
            sub_classification=result.get("classification", {}).get("sub_domain"),
            confidence=result.get("confidence", 0.0),
            needs_clarification=result.get("needs_clarification", False),
            sources=sources
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred processing your request: {str(e)}"
        )


async def create_new_session(user_id: str) -> str:
    """Create a new chat session for the user."""
    try:
        client = get_service_client()
        session_id = str(uuid.uuid4())
        
        client.table("chat_sessions").insert({
            "id": session_id,
            "user_id": user_id,
            "title": "New Conversation",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }).execute()
        
        return session_id
    except Exception as e:
        logger.error(f"Session creation error: {str(e)}")
        raise


async def validate_session_ownership(session_id: str, user_id: str):
    """Validate that the session belongs to the user."""
    try:
        client = get_service_client()
        result = client.table("chat_sessions").select("user_id").eq(
            "id", session_id
        ).single().execute()
        
        if not result.data or result.data["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Session not found or access denied"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )


async def update_session_timestamp(session_id: str):
    """Update the session's last updated timestamp."""
    try:
        client = get_service_client()
        client.table("chat_sessions").update({
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", session_id).execute()
    except Exception as e:
        logger.error(f"Session update error: {str(e)}")