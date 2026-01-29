"""
Embedding Functions
Uses HuggingFace Inference API for embeddings.
"""

from typing import List
import httpx
import asyncio

from app.config import settings
from app.utils.logger import logger


# HuggingFace Inference API endpoint
HF_INFERENCE_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction"


async def get_embedding(text: str) -> List[float]:
    """
    Get embedding vector for text using HuggingFace Inference API.
    
    Args:
        text: Text to embed
        
    Returns:
        Embedding vector as list of floats
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Truncate long texts
    text = text[:8000]
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{HF_INFERENCE_URL}/{settings.embedding_model}",
                headers={
                    "Authorization": f"Bearer {settings.hf_api_token_emb}",
                    "Content-Type": "application/json"
                },
                json={
                    "inputs": text,
                    "options": {
                        "wait_for_model": True
                    }
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Handle different response formats
            if isinstance(result, list):
                if isinstance(result[0], list):
                    # Nested list - take mean across tokens
                    import numpy as np
                    embedding = np.mean(result, axis=0).tolist()
                else:
                    embedding = result
            else:
                raise ValueError(f"Unexpected response format: {type(result)}")
            
            return embedding
            
    except httpx.HTTPError as e:
        logger.error(f"HuggingFace API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Embedding error: {str(e)}")
        raise


async def get_embeddings_batch(texts: List[str], batch_size: int = 10) -> List[List[float]]:
    """
    Get embeddings for multiple texts in batches.
    
    Args:
        texts: List of texts to embed
        batch_size: Number of texts to process in parallel
        
    Returns:
        List of embedding vectors
    """
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        # Process batch in parallel
        tasks = [get_embedding(text) for text in batch]
        batch_embeddings = await asyncio.gather(*tasks, return_exceptions=True)
        
        for emb in batch_embeddings:
            if isinstance(emb, Exception):
                logger.error(f"Batch embedding error: {str(emb)}")
                embeddings.append([0.0] * 384)  # Default dimension for MiniLM
            else:
                embeddings.append(emb)
    
    return embeddings


def get_embedding_sync(text: str) -> List[float]:
    """
    Synchronous wrapper for get_embedding.
    Used in non-async contexts.
    """
    return asyncio.run(get_embedding(text))