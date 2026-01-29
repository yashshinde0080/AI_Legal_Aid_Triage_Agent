"""
Document Embedder
Creates embeddings for document chunks.
"""

from typing import List, Dict, Any
import asyncio

from app.llm.embeddings import get_embedding, get_embeddings_batch
from app.utils.logger import logger


class DocumentEmbedder:
    """
    Creates embeddings for document chunks.
    Uses HuggingFace Inference API.
    """
    
    def __init__(self, batch_size: int = 10):
        """
        Initialize embedder.
        
        Args:
            batch_size: Number of documents to embed in parallel
        """
        self.batch_size = batch_size
    
    async def embed_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add embedding to a single document.
        
        Args:
            document: Document with content
            
        Returns:
            Document with embedding added
        """
        content = document.get("content", "")
        
        if not content:
            document["embedding"] = None
            return document
        
        try:
            embedding = await get_embedding(content)
            document["embedding"] = embedding
        except Exception as e:
            logger.error(f"Embedding error: {str(e)}")
            document["embedding"] = None
        
        return document
    
    async def embed_documents(
        self,
        documents: List[Dict[str, Any]],
        show_progress: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Add embeddings to multiple documents.
        
        Args:
            documents: List of documents
            show_progress: Whether to log progress
            
        Returns:
            Documents with embeddings added
        """
        total = len(documents)
        embedded_docs = []
        
        for i in range(0, total, self.batch_size):
            batch = documents[i:i + self.batch_size]
            
            # Get content for batch
            contents = [doc.get("content", "") for doc in batch]
            
            try:
                # Get embeddings for batch
                embeddings = await get_embeddings_batch(contents, self.batch_size)
                
                # Add embeddings to documents
                for doc, embedding in zip(batch, embeddings):
                    doc["embedding"] = embedding
                    embedded_docs.append(doc)
                
            except Exception as e:
                logger.error(f"Batch embedding error: {str(e)}")
                # Add documents without embeddings
                for doc in batch:
                    doc["embedding"] = None
                    embedded_docs.append(doc)
            
            if show_progress:
                progress = min(i + self.batch_size, total)
                logger.info(f"Embedded {progress}/{total} documents")
        
        successful = sum(1 for d in embedded_docs if d.get("embedding") is not None)
        logger.info(f"Successfully embedded {successful}/{total} documents")
        
        return embedded_docs
    
    def embed_documents_sync(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Synchronous wrapper for embed_documents.
        """
        return asyncio.run(self.embed_documents(documents))