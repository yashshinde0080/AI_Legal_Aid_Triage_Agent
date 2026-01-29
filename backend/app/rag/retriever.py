"""
Legal Document Retriever
High-level retriever for legal documents.
"""

from typing import List, Dict, Any, Optional

from app.db.vector import VectorStore
from app.utils.logger import logger


class LegalDocumentRetriever:
    """
    High-level retriever for legal documents.
    Provides domain-aware retrieval with filtering.
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
    
    async def retrieve(
        self,
        query: str,
        domain: Optional[str] = None,
        k: int = 5,
        min_score: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant legal documents.
        
        Args:
            query: Search query
            domain: Optional domain filter
            k: Number of documents to retrieve
            min_score: Minimum similarity score
            
        Returns:
            List of relevant documents
        """
        try:
            documents = await self.vector_store.similarity_search(
                query=query,
                k=k,
                filter_domain=domain,
                threshold=min_score
            )
            
            # Post-process and rank
            documents = self._post_process(documents)
            
            logger.info(f"Retrieved {len(documents)} documents for: {query[:50]}...")
            
            return documents
            
        except Exception as e:
            logger.error(f"Retrieval error: {str(e)}")
            return []
    
    async def retrieve_for_classification(
        self,
        domain: str,
        sub_domain: str,
        user_query: str,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve documents based on classification.
        
        Args:
            domain: Legal domain
            sub_domain: Sub-domain
            user_query: Original user query
            k: Number of documents
            
        Returns:
            List of relevant documents
        """
        # Build enhanced query
        enhanced_query = f"{domain} {sub_domain} procedure {user_query}"
        
        return await self.retrieve(
            query=enhanced_query,
            domain=domain,
            k=k
        )
    
    async def get_act_info(
        self,
        act_name: str,
        section: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific act.
        
        Args:
            act_name: Name of the act
            section: Optional section number
            
        Returns:
            Act information or None
        """
        query = act_name
        if section:
            query = f"{act_name} section {section}"
        
        documents = await self.retrieve(query=query, k=1, min_score=0.7)
        
        if documents:
            return documents[0]
        return None
    
    def _post_process(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Post-process retrieved documents.
        - Remove duplicates
        - Clean content
        - Add formatted citations
        """
        seen_content = set()
        processed = []
        
        for doc in documents:
            content = doc.get("content", "")
            
            # Simple deduplication based on content hash
            content_hash = hash(content[:200])
            if content_hash in seen_content:
                continue
            seen_content.add(content_hash)
            
            # Add formatted citation
            doc["citation"] = self._format_citation(doc)
            
            # Clean content
            doc["content"] = self._clean_content(content)
            
            processed.append(doc)
        
        return processed
    
    def _format_citation(self, doc: Dict[str, Any]) -> str:
        """Format a legal citation."""
        parts = []
        
        act_name = doc.get("act_name") or doc.get("title")
        if act_name:
            parts.append(act_name)
        
        section = doc.get("section")
        if section:
            parts.append(f"Section {section}")
        
        chapter = doc.get("chapter")
        if chapter:
            parts.append(f"Chapter {chapter}")
        
        return ", ".join(parts) if parts else "Legal Document"
    
    def _clean_content(self, content: str) -> str:
        """Clean document content."""
        import re
        
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove page numbers
        content = re.sub(r'\[\d+\]', '', content)
        content = re.sub(r'Page\s+\d+', '', content, flags=re.IGNORECASE)
        
        return content.strip()