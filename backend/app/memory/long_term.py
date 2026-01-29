"""
Long-term Memory
Persistent storage of conversation history in Supabase.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from app.db.supabase import get_supabase_client
from app.utils.logger import logger


async def save_message(
    session_id: str,
    role: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Save a message to the database.
    
    Args:
        session_id: Chat session ID
        role: Message role (user/assistant)
        content: Message content
        metadata: Optional metadata
        
    Returns:
        Message ID
    """
    try:
        client = get_supabase_client()
        
        message_id = str(uuid.uuid4())
        
        record = {
            "id": message_id,
            "session_id": session_id,
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat()
        }
        
        client.table("chat_messages").insert(record).execute()
        
        logger.debug(f"Saved message {message_id} to session {session_id}")
        
        return message_id
        
    except Exception as e:
        logger.error(f"Save message error: {str(e)}")
        raise


async def get_session_messages(
    session_id: str,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get messages for a session.
    
    Args:
        session_id: Chat session ID
        limit: Maximum messages to return
        offset: Offset for pagination
        
    Returns:
        List of messages
    """
    try:
        client = get_supabase_client()
        
        result = client.table("chat_messages").select(
            "id, role, content, metadata, created_at"
        ).eq(
            "session_id", session_id
        ).order(
            "created_at", desc=False
        ).range(offset, offset + limit - 1).execute()
        
        return result.data or []
        
    except Exception as e:
        logger.error(f"Get messages error: {str(e)}")
        return []


async def get_session_summary(session_id: str) -> Optional[str]:
    """
    Get the summary for a session.
    
    Args:
        session_id: Chat session ID
        
    Returns:
        Session summary or None
    """
    try:
        client = get_supabase_client()
        
        result = client.table("chat_sessions").select(
            "summary"
        ).eq("id", session_id).single().execute()
        
        if result.data:
            return result.data.get("summary")
        return None
        
    except Exception as e:
        logger.error(f"Get summary error: {str(e)}")
        return None


async def update_session_summary(session_id: str, summary: str) -> bool:
    """
    Update the summary for a session.
    
    Args:
        session_id: Chat session ID
        summary: New summary text
        
    Returns:
        Success status
    """
    try:
        client = get_supabase_client()
        
        client.table("chat_sessions").update({
            "summary": summary,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", session_id).execute()
        
        return True
        
    except Exception as e:
        logger.error(f"Update summary error: {str(e)}")
        return False


async def delete_session_messages(session_id: str) -> int:
    """
    Delete all messages for a session.
    
    Args:
        session_id: Chat session ID
        
    Returns:
        Number of deleted messages
    """
    try:
        client = get_supabase_client()
        
        result = client.table("chat_messages").delete().eq(
            "session_id", session_id
        ).execute()
        
        return len(result.data) if result.data else 0
        
    except Exception as e:
        logger.error(f"Delete messages error: {str(e)}")
        return 0


async def get_message_count(session_id: str) -> int:
    """
    Get the number of messages in a session.
    
    Args:
        session_id: Chat session ID
        
    Returns:
        Message count
    """
    try:
        client = get_supabase_client()
        
        result = client.table("chat_messages").select(
            "id", count="exact"
        ).eq("session_id", session_id).execute()
        
        return result.count or 0
        
    except Exception as e:
        logger.error(f"Get message count error: {str(e)}")
        return 0