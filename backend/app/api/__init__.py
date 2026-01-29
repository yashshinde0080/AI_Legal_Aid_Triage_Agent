"""
API Routes Module
Contains all FastAPI route handlers.
"""

from app.api import auth, chat, health, sessions

__all__ = ["auth", "chat", "health", "sessions"]