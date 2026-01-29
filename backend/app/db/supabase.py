"""
Supabase Client Configuration
Singleton pattern for database connection.
"""

from supabase import create_client, Client
from typing import Optional

from app.config import settings
from app.utils.logger import logger


_supabase_client: Optional[Client] = None


def init_supabase() -> Client:
    """
    Initialize Supabase client.
    Called once during application startup.
    """
    global _supabase_client
    
    try:
        _supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        logger.info("Supabase client initialized successfully")
        return _supabase_client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase: {str(e)}")
        raise


def get_supabase_client() -> Client:
    """
    Get the Supabase client instance.
    Initializes if not already done.
    """
    global _supabase_client
    
    if _supabase_client is None:
        return init_supabase()
    
    return _supabase_client


def get_service_client() -> Client:
    """
    Get Supabase client with service role key.
    Used for admin operations.
    """
    return create_client(
        settings.supabase_url,
        settings.supabase_service_key
    )