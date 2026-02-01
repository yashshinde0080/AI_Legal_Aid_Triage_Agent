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
    metadata: Optional[Dict[str, Any]]


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
    clarification_count = 0
    
    if chat_history:
        for msg in chat_history:
            formatted_history.append(ChatMessage(
                role=msg.get("role", "user"),
                content=msg.get("content", ""),
                timestamp=msg.get("created_at", datetime.utcnow().isoformat()),
                metadata=msg.get("metadata", {})
            ))
            
        # Calculate current clarification loop count
        # Count consecutive assistant messages at the end that needed clarification
        # We look at the history in reverse
        for i in range(len(formatted_history) - 1, -1, -1):
            msg = formatted_history[i]
            if msg["role"] == "assistant":
                meta = msg.get("metadata", {})
                if meta and meta.get("needs_clarification"):
                    clarification_count += 1
                else:
                    # Break if we hit a non-clarification assistant message
                    # But we also need to consider user messages in between?
                    # Actually, for a loop: Assistant (Clarify) -> User (Answer) -> Assistant (Clarify) -> ...
                    # So we should count how many times this pattern has happened recently.
                    # Or simpler: just count how many previous turns were clarification.
                    pass
            elif msg["role"] == "user":
                # User message doesn't break the loop count itself, it's part of the loop
                pass
            else:
                # Break on other roles if any
                pass
                
        # Refined logic: Count pairs of (Assistant Clarification -> User Answer)
        # But formatted_history is just a list.
        # Let's just count total clarifications in the recent contiguous block of conversation
        # excluding the very first message maybe?
        
        # Simpler robust logic:
        # Just count how many messages in the last X messages have "needs_clarification"=True.
        # Since the user wants to limit the TOTAL questions, tracking the total in the recent context is fine.
        count = 0
        for msg in reversed(formatted_history):
            if msg["role"] == "assistant":
                if msg.get("metadata", {}).get("needs_clarification"):
                    count += 1
                else:
                    # If we find an assistant message that was a result (not clarification), reset count?
                    # Yes, because that means a previous loop ended.
                    break
        clarification_count = count
    
    return LegalAgentState(
        user_input=user_input,
        session_id=session_id,
        user_id=user_id,
        chat_history=formatted_history,
        classification=None,
        confidence=0.0,
        retrieved_docs=[],
        needs_clarification=False,
        clarification_count=clarification_count,
        clarification_question=None,
        response="",
        current_node="start",
        error=None,
        logs=[]
    )