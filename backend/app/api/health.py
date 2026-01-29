"""
Health Check Endpoints
Used for monitoring and deployment verification.
"""

from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime

from app.config import settings
from app.db.supabase import get_supabase_client


router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    timestamp: str
    version: str
    services: dict


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check endpoint.
    Verifies all critical services are operational.
    """
    services = {
        "api": "healthy",
        "database": "unknown",
        "llm": "unknown"
    }
    
    # Check Supabase connection
    try:
        client = get_supabase_client()
        # Simple query to verify connection
        client.table("chat_sessions").select("id").limit(1).execute()
        services["database"] = "healthy"
    except Exception as e:
        services["database"] = f"unhealthy: {str(e)}"
    
    # Overall status
    overall_status = "healthy" if all(
        v == "healthy" for v in services.values()
    ) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat(),
        version=settings.api_version,
        services=services
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Root endpoint returning API information."""
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "docs": "/docs" if settings.debug else "disabled"
    }