"""
Vector Store Operations
Handles pgvector operations for RAG.
"""

from typing import List, Dict, Any, Optional
import json
import uuid

from app.db.supabase import get_service_client
from app.llm.embeddings import get_embedding
from app.utils.logger import logger


class VectorStore:
    """
    Vector store for legal document embeddings.
    Uses Supabase pgvector for similarity search.
    """
    
    TABLE_NAME = "legal_chunks"
    
    def __init__(self):
        # Use service client to bypass RLS for ingestion
        self.client = get_service_client()
    
    async def add_documents(
        self,
        documents: List[Dict[str, Any]],
        batch_size: int = 100
    ) -> int:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents with content and metadata
            batch_size: Number of documents to process at once
            
        Returns:
            Number of documents added
        """
        added_count = 0
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            for doc in batch:
                try:
                    # Check for existing embedding
                    if "embedding" not in doc or doc["embedding"] is None:
                        logger.warning(f"Document missing embedding, skipping: {doc.get('act_name', 'Unknown')}")
                        continue
                        
                    # Prepare record
                    record = {
                        "content": doc["content"],
                        "embedding": doc["embedding"],
                        "act_name": doc.get("act_name"),
                        "section": doc.get("section"),
                        "chapter": doc.get("chapter"),
                        "source_url": doc.get("source_url"),
                        "domain": doc.get("domain"),
                        "metadata": json.dumps(doc.get("metadata", {}))
                    }
                    
                    # Insert into database
                    self.client.table(self.TABLE_NAME).insert(record).execute()
                    added_count += 1
                    
                except Exception as e:
                    logger.error(f"Error adding document: {str(e)}")
                    continue
        
        logger.info(f"Added {added_count} documents to vector store")
        return added_count
    
    async def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter_domain: Optional[str] = None,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_domain: Optional domain filter
            threshold: Minimum similarity threshold
            
        Returns:
            List of matching documents with scores
        """
        try:
            # Generate query embedding
            query_embedding = await get_embedding(query)
            
            # Build the RPC call for vector similarity search
            # This uses a Supabase function for cosine similarity
            result = self.client.rpc(
                "match_legal_chunks",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": threshold,
                    "match_count": k,
                    "filter_domain": filter_domain
                }
            ).execute()
            
            if not result.data:
                return []
            
            # Format results
            documents = []
            for row in result.data:
                documents.append({
                    "id": row["id"],
                    "content": row["content"],
                    "score": row["similarity"],
                    "act_name": row.get("act_name"),
                    "section": row.get("section"),
                    "chapter": row.get("chapter"),
                    "source_url": row.get("source_url"),
                    "domain": row.get("domain"),
                    "metadata": json.loads(row.get("metadata", "{}"))
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Similarity search error: {str(e)}")
            # Fallback to basic text search if vector search fails
            return await self._fallback_search(query, k, filter_domain)
    
    async def _fallback_search(
        self,
        query: str,
        k: int = 5,
        filter_domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fallback text search when vector search fails.
        """
        try:
            query_builder = self.client.table(self.TABLE_NAME).select(
                "id, content, act_name, section, chapter, source_url, domain, metadata"
            ).ilike("content", f"%{query}%").limit(k)
            
            if filter_domain:
                query_builder = query_builder.eq("domain", filter_domain)
            
            result = query_builder.execute()
            
            return [
                {
                    "id": row["id"],
                    "content": row["content"],
                    "score": 0.5,  # Default score for text search
                    "act_name": row.get("act_name"),
                    "section": row.get("section"),
                    "chapter": row.get("chapter"),
                    "source_url": row.get("source_url"),
                    "domain": row.get("domain"),
                    "metadata": json.loads(row.get("metadata", "{}"))
                }
                for row in result.data
            ]
            
        except Exception as e:
            logger.error(f"Fallback search error: {str(e)}")
            return []
    
    async def delete_by_domain(self, domain: str) -> int:
        """
        Delete all documents for a specific domain.
        
        Args:
            domain: Domain to delete
            
        Returns:
            Number of documents deleted
        """
        try:
            result = self.client.table(self.TABLE_NAME).delete().eq(
                "domain", domain
            ).execute()
            
            deleted_count = len(result.data) if result.data else 0
            logger.info(f"Deleted {deleted_count} documents from domain: {domain}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Delete by domain error: {str(e)}")
            return 0
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        """
        try:
            # Get total count
            total_result = self.client.table(self.TABLE_NAME).select(
                "id", count="exact"
            ).execute()
            
            # Get counts by domain
            domain_result = self.client.table(self.TABLE_NAME).select(
                "domain"
            ).execute()
            
            domain_counts = {}
            for row in domain_result.data:
                domain = row.get("domain", "unknown")
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
            
            return {
                "total_documents": total_result.count or 0,
                "domains": domain_counts
            }
            
        except Exception as e:
            logger.error(f"Get stats error: {str(e)}")
            return {"total_documents": 0, "domains": {}}