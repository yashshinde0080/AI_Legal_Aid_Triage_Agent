"""
Database Models
Pydantic models for database tables.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatSession(BaseModel):
    """Chat session model."""
    id: str
    user_id: str
    title: str = "New Conversation"
    summary: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    """Chat message model."""
    id: str
    session_id: str
    role: MessageRole
    content: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True


class LegalChunk(BaseModel):
    """Legal document chunk model for vector storage."""
    id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Metadata fields
    act_name: Optional[str] = None
    section: Optional[str] = None
    chapter: Optional[str] = None
    source_url: Optional[str] = None
    domain: Optional[str] = None
    
    class Config:
        from_attributes = True


class AgentLog(BaseModel):
    """Agent execution log model."""
    id: str
    session_id: str
    user_id: str
    node_name: str
    input_state: Dict[str, Any]
    output_state: Dict[str, Any]
    duration_ms: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True