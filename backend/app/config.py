"""
Application configuration using Pydantic Settings.
All environment variables are validated and typed.
"""

import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="LegalAidTriage")
    debug: bool = Field(default=False)
    api_version: str = Field(default="v1")
    
    # Supabase
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_key: str = Field(..., env="SUPABASE_KEY")
    supabase_service_key: str = Field(..., env="SUPABASE_SERVICE_KEY")
    
    # LLM Providers
    llm_provider: str = Field(default="gemini", env="LLM_PROVIDER")
    google_api_key: str = Field(default="", env="GOOGLE_API_KEY")
    openrouter_api_key: str = Field(default="", env="OPENROUTER_API_KEY")
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    hf_api_token: str = Field(default="", env="HF_API_TOKEN")
    xai_api_key: str = Field(default="", env="XAI_API_KEY")
    
    # Embeddings
    hf_api_token_emb: str = Field(default="", env="HF_API_TOKEN_EMB")
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        env="EMBEDDING_MODEL"
    )
    
    # Agent Settings
    confidence_threshold: float = Field(default=0.7, env="CONFIDENCE_THRESHOLD")
    max_clarification_loops: int = Field(default=15, env="MAX_CLARIFICATION_LOOPS")
    max_context_messages: int = Field(default=10, env="MAX_CONTEXT_MESSAGES")
    
    # Security
    jwt_secret: str = Field(default="dev-secret-change-in-prod", env="JWT_SECRET")
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        env="CORS_ORIGINS"
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid reloading env vars on every request.
    """
    return Settings()


# Global settings instance
settings = get_settings()
# Trigger reload for .env update