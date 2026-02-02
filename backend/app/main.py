"""
FastAPI Application Entry Point
Main application setup with middleware, routes, and lifecycle events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import auth, chat, health, sessions
from app.utils.logger import setup_logger, logger
from app.db.supabase import init_supabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.api_version}")
    setup_logger()
    init_supabase()
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Application shutting down")


def create_app() -> FastAPI:
    """
    Application factory pattern.
    Creates and configures the FastAPI application.
    """
    app = FastAPI(
        title=settings.app_name,
        description="AI Legal Aid Triage Agent - Stateful legal triage system",
        version=settings.api_version,
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
    app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )