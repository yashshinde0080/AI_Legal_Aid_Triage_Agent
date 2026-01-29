"""
LLM Router
Provides pluggable LLM backend support.
"""

from enum import Enum
from typing import Optional
from langchain_core.language_models import BaseChatModel

from app.config import settings
from app.utils.logger import logger


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    GEMINI = "gemini"
    OPENROUTER = "openrouter"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    XAI = "xai"


def get_llm(provider: Optional[str] = None) -> BaseChatModel:
    """
    Get LLM instance based on provider.
    
    Args:
        provider: LLM provider name. Uses default from settings if None.
        
    Returns:
        Configured LLM instance.
        
    Raises:
        ValueError: If provider is not supported or not configured.
    """
    provider = provider or settings.llm_provider
    provider = provider.lower()
    
    logger.info(f"Initializing LLM with provider: {provider}")
    
    if provider == LLMProvider.GEMINI:
        return _get_gemini_llm()
    
    if provider == LLMProvider.OPENROUTER:
        return _get_openrouter_llm()
    
    if provider == LLMProvider.OPENAI:
        return _get_openai_llm()
    
    if provider == LLMProvider.HUGGINGFACE:
        return _get_huggingface_llm()
    
    if provider == LLMProvider.XAI:
        return _get_xai_llm()
    
    raise ValueError(f"Unsupported LLM provider: {provider}")


def _get_gemini_llm() -> BaseChatModel:
    """Get Google Gemini LLM instance."""
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY not configured")
    
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=settings.google_api_key,
        temperature=0,
        max_output_tokens=2048,
        convert_system_message_to_human=True
    )


def _get_openrouter_llm() -> BaseChatModel:
    """Get OpenRouter LLM instance."""
    if not settings.openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY not configured")
    
    from langchain_openai import ChatOpenAI
    
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
        model="mistralai/mistral-7b-instruct",
        temperature=0,
        max_tokens=2048
    )


def _get_openai_llm() -> BaseChatModel:
    """Get OpenAI LLM instance."""
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY not configured")
    
    from langchain_openai import ChatOpenAI
    
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=2048
    )


def _get_huggingface_llm() -> BaseChatModel:
    """Get HuggingFace LLM instance."""
    if not settings.hf_api_token:
        raise ValueError("HF_API_TOKEN not configured")
    
    from langchain_community.llms import HuggingFaceHub
    from langchain_core.language_models import BaseChatModel
    from langchain.chat_models import ChatHuggingFace
    
    # Use Zephyr as the chat model
    llm = HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        huggingfacehub_api_token=settings.hf_api_token,
        model_kwargs={
            "temperature": 0.1,
            "max_new_tokens": 2048
        }
    )
    
    return llm


def _get_xai_llm() -> BaseChatModel:
    """Get xAI (Grok) LLM instance."""
    if not settings.xai_api_key:
        raise ValueError("XAI_API_KEY not configured")
    
    from langchain_openai import ChatOpenAI
    
    return ChatOpenAI(
        base_url="https://api.x.ai/v1",
        api_key=settings.xai_api_key,
        model="grok-beta",
        temperature=0,
        max_tokens=2048
    )


# Provider availability check
def get_available_providers() -> list[str]:
    """Get list of configured and available LLM providers."""
    available = []
    
    if settings.google_api_key:
        available.append(LLMProvider.GEMINI)
    if settings.openrouter_api_key:
        available.append(LLMProvider.OPENROUTER)
    if settings.openai_api_key:
        available.append(LLMProvider.OPENAI)
    if settings.hf_api_token:
        available.append(LLMProvider.HUGGINGFACE)
    if settings.xai_api_key:
        available.append(LLMProvider.XAI)
    
    return available