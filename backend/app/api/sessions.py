"""
Session Management API Endpoints
Handles chat session CRUD operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.api.auth import get_current_user
from app.db.supabase import get_supabase_client
from app.utils.logger import logger


router = APIRouter()


class SessionResponse(BaseModel):
    """Session response schema."""
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int = 0
    last_message: Optional[str] = None


class SessionUpdateRequest(BaseModel):
    """Session update request schema."""
    title: str = Field(..., min_length=1, max_length=200)


class MessageResponse(BaseModel):
    """Message response schema."""
    id: str
    role: str
    content: str
    created_at: str
    metadata: Optional[dict] = None


@router.get("", response_model=List[SessionResponse])
async def list_sessions(user: dict = Depends(get_current_user)):
    """
    List all chat sessions for the current user.
    Returns sessions ordered by last updated.
    """
    try:
        client = get_supabase_client()
        
        # Get sessions
        sessions_result = client.table("chat_sessions").select(
            "id, title, created_at, updated_at"
        ).eq("user_id", user["id"]).order(
            "updated_at", desc=True
        ).execute()
        
        sessions = []
        for session in sessions_result.data:
            # Get message count and last message
            messages_result = client.table("chat_messages").select(
                "content"
            ).eq("session_id", session["id"]).order(
                "created_at", desc=True
            ).limit(1).execute()
            
            message_count_result = client.table("chat_messages").select(
                "id", count="exact"
            ).eq("session_id", session["id"]).execute()
            
            last_message = None
            if messages_result.data:
                last_message = messages_result.data[0]["content"][:100]
            
            sessions.append(SessionResponse(
                id=session["id"],
                title=session["title"],
                created_at=session["created_at"],
                updated_at=session["updated_at"],
                message_count=message_count_result.count or 0,
                last_message=last_message
            ))
        
        return sessions
        
    except Exception as e:
        logger.error(f"List sessions error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sessions"
        )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, user: dict = Depends(get_current_user)):
    """
    Get a specific chat session.
    """
    try:
        client = get_supabase_client()
        
        result = client.table("chat_sessions").select(
            "id, title, created_at, updated_at, user_id"
        ).eq("id", session_id).single().execute()
        
        if not result.data or result.data["user_id"] != user["id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get message count
        message_count_result = client.table("chat_messages").select(
            "id", count="exact"
        ).eq("session_id", session_id).execute()
        
        return SessionResponse(
            id=result.data["id"],
            title=result.data["title"],
            created_at=result.data["created_at"],
            updated_at=result.data["updated_at"],
            message_count=message_count_result.count or 0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get session error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve session"
        )


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: str, 
    user: dict = Depends(get_current_user),
    limit: int = 50,
    offset: int = 0
):
    """
    Get messages for a specific chat session.
    """
    try:
        client = get_supabase_client()
        
        # Verify session ownership
        session_result = client.table("chat_sessions").select(
            "user_id"
        ).eq("id", session_id).single().execute()
        
        if not session_result.data or session_result.data["user_id"] != user["id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get messages
        messages_result = client.table("chat_messages").select(
            "id, role, content, created_at, metadata"
        ).eq("session_id", session_id).order(
            "created_at", desc=False
        ).range(offset, offset + limit - 1).execute()
        
        return [
            MessageResponse(
                id=msg["id"],
                role=msg["role"],
                content=msg["content"],
                created_at=msg["created_at"],
                metadata=msg.get("metadata")
            )
            for msg in messages_result.data
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get messages error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages"
        )


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    request: SessionUpdateRequest,
    user: dict = Depends(get_current_user)
):
    """
    Update a chat session's title.
    """
    try:
        client = get_supabase_client()
        
        # Verify session ownership
        session_result = client.table("chat_sessions").select(
            "user_id"
        ).eq("id", session_id).single().execute()
        
        if not session_result.data or session_result.data["user_id"] != user["id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Update session
        update_result = client.table("chat_sessions").update({
            "title": request.title,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", session_id).execute()
        
        return SessionResponse(
            id=session_id,
            title=request.title,
            created_at=session_result.data.get("created_at", ""),
            updated_at=datetime.utcnow().isoformat(),
            message_count=0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update session error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update session"
        )


@router.delete("/{session_id}")
async def delete_session(session_id: str, user: dict = Depends(get_current_user)):
    """
    Delete a chat session and all its messages.
    """
    try:
        client = get_supabase_client()
        
        # Verify session ownership
        session_result = client.table("chat_sessions").select(
            "user_id"
        ).eq("id", session_id).single().execute()
        
        if not session_result.data or session_result.data["user_id"] != user["id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Delete messages first (foreign key constraint)
        client.table("chat_messages").delete().eq(
            "session_id", session_id
        ).execute()
        
        # Delete session
        client.table("chat_sessions").delete().eq(
            "id", session_id
        ).execute()
        
        return {"message": "Session deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete session error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete session"
        )