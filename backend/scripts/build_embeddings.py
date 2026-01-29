"""
Build Embeddings Script
Rebuilds embeddings for all documents in the vector store.
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.supabase import get_supabase_client
from app.llm.embeddings import get_embedding
from app.utils.logger import setup_logger, logger


async def rebuild_embeddings(batch_size: int = 10):
    """
    Rebuild embeddings for all documents.
    
    Args:
        batch_size: Number of documents to process at once
    """
    setup_logger()
    logger.info("Starting embedding rebuild...")
    
    client = get_supabase_client()
    
    # Get all documents without embeddings or all documents
    result = client.table("legal_chunks").select(
        "id, content"
    ).is_("embedding", "null").execute()
    
    documents = result.data
    total = len(documents)
    
    if total == 0:
        logger.info("No documents need embedding")
        return
    
    logger.info(f"Found {total} documents to embed")
    
    success_count = 0
    error_count = 0
    
    for i in range(0, total, batch_size):
        batch = documents[i:i + batch_size]
        
        for doc in batch:
            try:
                embedding = await get_embedding(doc["content"])
                
                client.table("legal_chunks").update({
                    "embedding": embedding
                }).eq("id", doc["id"]).execute()
                
                success_count += 1
                
            except Exception as e:
                logger.error(f"Error embedding document {doc['id']}: {str(e)}")
                error_count += 1
        
        progress = min(i + batch_size, total)
        logger.info(f"Progress: {progress}/{total} ({success_count} success, {error_count} errors)")
    
    logger.info(f"Embedding rebuild complete: {success_count} success, {error_count} errors")


async def verify_embeddings():
    """Verify all documents have embeddings."""
    setup_logger()
    
    client = get_supabase_client()
    
    # Count documents with embeddings
    with_embedding = client.table("legal_chunks").select(
        "id", count="exact"
    ).not_.is_("embedding", "null").execute()
    
    # Count documents without embeddings
    without_embedding = client.table("legal_chunks").select(
        "id", count="exact"
    ).is_("embedding", "null").execute()
    
    logger.info(f"Documents with embeddings: {with_embedding.count}")
    logger.info(f"Documents without embeddings: {without_embedding.count}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        asyncio.run(verify_embeddings())
    else:
        asyncio.run(rebuild_embeddings())