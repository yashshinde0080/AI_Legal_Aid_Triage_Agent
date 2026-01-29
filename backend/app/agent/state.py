"""
Agent State Definition
Core state schema for the LangGraph agent.
"""

from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime


class ClassificationResult(TypedDict):
    """Legal issue classification result."""
    domain: str
    sub_domain: str
    confidence: float
    missing_fields: List[str]


class RetrievedDocument(TypedDict):
    """Retrieved legal document."""
    id: str
    content: str
    title: str
    section: str
    source_url: Optional[str]
    score: float


class ChatMessage(TypedDict):
    """Chat message structure."""
    role: str
    content: str
    timestamp: str


class LegalAgentState(TypedDict):
    """
    Main agent state.
    This is the single source of truth for the agent loop.
    """
    # Input
    user_input: str
    session_id: str
    user_id: str
    
    # Context
    chat_history: List[ChatMessage]
    
    # Classification
    classification: Optional[ClassificationResult]
    confidence: float
    
    # Retrieval
    retrieved_docs: List[RetrievedDocument]
    
    # Control flow
    needs_clarification: bool
    clarification_count: int
    clarification_question: Optional[str]
    
    # Output
    response: str
    
    # Metadata
    current_node: str
    error: Optional[str]
    
    # Audit
    logs: List[Dict[str, Any]]


def create_initial_state(
    user_input: str,
    session_id: str,
    user_id: str,
    chat_history: Optional[List[Dict[str, Any]]] = None
) -> LegalAgentState:
    """
    Create initial agent state for a new request.
    
    Args:
        user_input: User's message
        session_id: Chat session ID
        user_id: User ID
        chat_history: Previous messages in the session
        
    Returns:
        Initialized LegalAgentState
    """
    # Convert chat history to proper format
    formatted_history = []
    if chat_history:
        for msg in chat_history:
            formatted_history.append(ChatMessage(
                role=msg.get("role", "user"),
                content=msg.get("content", ""),
                timestamp=msg.get("created_at", datetime.utcnow().isoformat())
            ))
    
    return LegalAgentState(
        user_input=user_input,
        session_id=session_id,
        user_id=user_id,
        chat_history=formatted_history,
        classification=None,
        confidence=0.0,
        retrieved_docs=[],
        needs_clarification=False,
        clarification_count=0,
        clarification_question=None,
        response="",
        current_node="start",
        error=None,
        logs=[]
    )