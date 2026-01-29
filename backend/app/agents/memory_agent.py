"""
Memory Agent
Handles conversation memory management.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from app.memory.long_term import (
    save_message,
    get_session_messages,
    get_session_summary,
    update_session_summary
)
from app.config import settings
from app.utils.logger import logger


SUMMARIZATION_PROMPT = """Summarize this legal aid conversation concisely.
Focus on:
1. The main legal issue discussed
2. Classification/domain identified
3. Key procedural guidance provided
4. Any clarifications made
5. Current status/next steps

Keep the summary under 200 words.

Conversation:
{conversation}

Summary:
"""


class MemoryAgent:
    """
    Memory Agent: Manages ChatGPT-like conversation memory.
    
    Responsibilities:
    - Write messages to long-term memory
    - Summarize old context
    - Load session history
    - Control token growth
    """
    
    def __init__(self, llm: BaseChatModel = None):
        self.llm = llm
        self.max_messages = settings.max_context_messages
    
    async def save(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Save a message to memory.
        
        Args:
            session_id: Session ID
            role: Message role (user/assistant)
            content: Message content
            metadata: Optional metadata
            
        Returns:
            Success status
        """
        try:
            await save_message(
                session_id=session_id,
                role=role,
                content=content,
                metadata=metadata
            )
            
            # Check if summarization needed
            await self._check_and_summarize(session_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Memory save error: {str(e)}")
            return False
    
    async def load(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Load conversation history.
        
        Args:
            session_id: Session ID
            limit: Maximum messages to load
            
        Returns:
            List of messages
        """
        try:
            limit = limit or self.max_messages
            messages = await get_session_messages(session_id, limit=limit)
            
            # Get summary if available
            summary = await get_session_summary(session_id)
            
            if summary:
                # Prepend summary as context
                messages.insert(0, {
                    "role": "system",
                    "content": f"Previous conversation summary: {summary}",
                    "created_at": datetime.utcnow().isoformat()
                })
            
            return messages
            
        except Exception as e:
            logger.error(f"Memory load error: {str(e)}")
            return []
    
    async def _check_and_summarize(self, session_id: str):
        """Check if summarization is needed and perform it."""
        if not self.llm:
            return
        
        try:
            # Get message count
            messages = await get_session_messages(session_id, limit=100)
            
            # Summarize if more than 20 messages
            if len(messages) > 20:
                await self._summarize_session(session_id, messages)
                
        except Exception as e:
            logger.warning(f"Summarization check error: {str(e)}")
    
    async def _summarize_session(
        self,
        session_id: str,
        messages: List[Dict[str, Any]]
    ):
        """Summarize older messages."""
        try:
            # Format conversation for summarization
            conversation_text = self._format_conversation(messages[:-10])  # Keep last 10
            
            prompt = SUMMARIZATION_PROMPT.format(conversation=conversation_text)
            
            llm_messages = [
                SystemMessage(content="You are a conversation summarizer."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(llm_messages)
            summary = response.content.strip()
            
            # Save summary
            await update_session_summary(session_id, summary)
            
            logger.info(f"Session {session_id} summarized")
            
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
    
    def _format_conversation(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages for summarization."""
        formatted = []
        for msg in messages:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")[:500]
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    async def clear_session(self, session_id: str) -> bool:
        """Clear all messages from a session."""
        try:
            from app.db.supabase import get_supabase_client
            client = get_supabase_client()
            
            client.table("chat_messages").delete().eq(
                "session_id", session_id
            ).execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Clear session error: {str(e)}")
            return False
    
    def estimate_tokens(self, messages: List[Dict[str, Any]]) -> int:
        """Estimate token count for messages."""
        total_chars = sum(len(msg.get("content", "")) for msg in messages)
        # Rough estimate: 4 chars per token
        return total_chars // 4