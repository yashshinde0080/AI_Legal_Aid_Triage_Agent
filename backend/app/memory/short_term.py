"""
Short-term Memory
In-memory conversation buffer for the current session.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque


class ConversationMemory:
    """
    Short-term conversation memory.
    Maintains a buffer of recent messages for context.
    """
    
    def __init__(self, max_messages: int = 20):
        """
        Initialize conversation memory.
        
        Args:
            max_messages: Maximum messages to keep in memory
        """
        self.max_messages = max_messages
        self._messages: deque = deque(maxlen=max_messages)
    
    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add a message to memory.
        
        Args:
            role: Message role (user/assistant/system)
            content: Message content
            metadata: Optional metadata
        """
        message = {
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self._messages.append(message)
    
    def add_user_message(self, content: str):
        """Add a user message."""
        self.add_message("user", content)
    
    def add_assistant_message(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add an assistant message."""
        self.add_message("assistant", content, metadata)
    
    def get_messages(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get messages from memory.
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of messages
        """
        messages = list(self._messages)
        if limit:
            messages = messages[-limit:]
        return messages
    
    def get_context_string(self, max_chars: int = 4000) -> str:
        """
        Get messages formatted as a context string.
        
        Args:
            max_chars: Maximum characters to include
            
        Returns:
            Formatted context string
        """
        messages = self.get_messages()
        parts = []
        total_chars = 0
        
        # Start from most recent
        for msg in reversed(messages):
            role = msg["role"].capitalize()
            content = msg["content"]
            part = f"{role}: {content}"
            
            if total_chars + len(part) > max_chars:
                break
            
            parts.insert(0, part)
            total_chars += len(part)
        
        return "\n".join(parts)
    
    def get_last_message(self) -> Optional[Dict[str, Any]]:
        """Get the most recent message."""
        if self._messages:
            return self._messages[-1]
        return None
    
    def get_last_user_message(self) -> Optional[str]:
        """Get the most recent user message content."""
        for msg in reversed(self._messages):
            if msg["role"] == "user":
                return msg["content"]
        return None
    
    def clear(self):
        """Clear all messages from memory."""
        self._messages.clear()
    
    def to_langchain_messages(self) -> List:
        """
        Convert to LangChain message format.
        
        Returns:
            List of LangChain messages
        """
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
        
        lc_messages = []
        for msg in self._messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "user":
                lc_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
            elif role == "system":
                lc_messages.append(SystemMessage(content=content))
        
        return lc_messages
    
    def __len__(self) -> int:
        return len(self._messages)
    
    def __bool__(self) -> bool:
        return len(self._messages) > 0