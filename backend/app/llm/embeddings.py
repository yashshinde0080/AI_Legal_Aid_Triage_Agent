"""
Embedding Functions
Uses local SentenceTransformer for embeddings (unified with ingestion).
"""

from typing import List, Optional
import asyncio
from app.rag.embedder import DocumentEmbedder
from app.utils.logger import logger

# Global instance to load model once into memory
_global_embedder: Optional[DocumentEmbedder] = None

def get_embedder_instance() -> DocumentEmbedder:
    """Singleton pattern for the embedder model."""
    global _global_embedder
    if _global_embedder is None:
        logger.info("Initializing global SentenceTransformer model...")
        _global_embedder = DocumentEmbedder()
    return _global_embedder

async def get_embedding(text: str) -> List[float]:
    """
    Get embedding vector for text using local model.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    embedder = get_embedder_instance()
    
    # Reuse the logic in DocumentEmbedder, but for a single string.
    # To keep it efficient, we wrap it in a pseudo-document structure 
    # or expose a direct method on DocumentEmbedder.
    # Since DocumentEmbedder expects list[dict], let's create a helper there or just use it here.
    
    # Better: Use the thread pool execution from the embedder instance
    loop = asyncio.get_running_loop()
    
    # model.encode can take a single string
    embedding = await loop.run_in_executor(
        None,
        lambda: embedder.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
    )
    
    return embedding.tolist()


async def get_embeddings_batch(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Get embeddings for multiple texts using local model.
    """
    if not texts:
        return []

    embedder = get_embedder_instance()
    loop = asyncio.get_running_loop()
    
    embeddings = await loop.run_in_executor(
        None,
        lambda: embedder.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
    )
    
    return embeddings.tolist()


def get_embedding_sync(text: str) -> List[float]:
    """
    Synchronous wrapper for get_embedding.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
        
    embedder = get_embedder_instance()
    embedding = embedder.model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embedding.tolist()