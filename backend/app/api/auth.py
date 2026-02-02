"""
Authentication API Endpoints
Handles user authentication via Supabase Auth.
"""

import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel, EmailStr

from app.db.supabase import get_supabase_client
from app.utils.logger import logger


router = APIRouter()


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    """Signup request schema."""
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class AuthResponse(BaseModel):
    """Authentication response schema."""
    access_token: str
    refresh_token: str
    user_id: str
    email: str


class UserResponse(BaseModel):
    """User information response schema."""
    id: str
    email: str
    full_name: Optional[str] = None
    created_at: str


def get_current_user(authorization: str = Header(...)) -> dict:
    """
    Dependency to get current authenticated user from JWT.
    Validates the Supabase JWT token.
    Uses sync def to run in threadpool as Supabase client is synchronous.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    token = authorization.replace("Bearer ", "")
    
    # Retry mechanism for Supabase connection (SSL handshake timeouts)
    max_retries = 3
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            client = get_supabase_client()
            # client.auth.get_user creates a network request using httpx (sync)
            user_response = client.auth.get_user(token)
            
            if not user_response or not user_response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )
            
            return {
                "id": user_response.user.id,
                "email": user_response.user.email,
                "full_name": user_response.user.user_metadata.get("full_name")
            }
        except HTTPException:
            # If it's an HTTP exception (e.g. 401 from supabase), re-raise immediately
            raise
        except Exception as e:
            last_exception = e
            # Log warning and retry if it's a network error
            if attempt < max_retries - 1:
                logger.warning(f"Authentication attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                time.sleep(0.5)  # Short backoff
    
    logger.error(f"Authentication final error: {str(last_exception)}")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication failed"
    )


@router.post("/signup", response_model=AuthResponse)
def signup(request: SignupRequest):
    """
    Register a new user.
    Creates user in Supabase Auth.
    """
    try:
        client = get_supabase_client()
        
        auth_response = client.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "full_name": request.full_name
                }
            }
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Signup failed"
            )
        
        return AuthResponse(
            access_token=auth_response.session.access_token,
            refresh_token=auth_response.session.refresh_token,
            user_id=auth_response.user.id,
            email=auth_response.user.email
        )
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest):
    """
    Authenticate existing user.
    Returns JWT tokens for subsequent requests.
    """
    try:
        client = get_supabase_client()
        
        auth_response = client.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        return AuthResponse(
            access_token=auth_response.session.access_token,
            refresh_token=auth_response.session.refresh_token,
            user_id=auth_response.user.id,
            email=auth_response.user.email
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@router.post("/logout")
def logout(user: dict = Depends(get_current_user)):
    """
    Logout current user.
    Invalidates the current session.
    """
    try:
        client = get_supabase_client()
        client.auth.sign_out()
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return {"message": "Logged out"}


@router.get("/me", response_model=UserResponse)
def get_me(user: dict = Depends(get_current_user)):
    """
    Get current user information.
    Requires valid JWT token.
    """
    return UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user.get("full_name"),
        created_at=datetime.utcnow().isoformat()
    )