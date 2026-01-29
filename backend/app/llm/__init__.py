"""
LLM Module
Contains LLM router and embedding functions.
"""

from app.llm.router import get_llm, LLMProvider
from app.llm.embeddings import get_embedding

__all__ = ["get_llm", "LLMProvider", "get_embedding"]