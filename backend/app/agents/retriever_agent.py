"""
Retriever Agent
Handles retrieval of relevant legal documents.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from app.db.vector import VectorStore
from app.utils.logger import logger


class RetrieverAgent:
    """
    Retriever Agent: Retrieves relevant legal documents via RAG.
    
    Responsibilities:
    - Query pgvector for relevant documents
    - Retrieve only verified legal sources
    - Return act + section + procedure
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.default_k = 5
    
    async def retrieve(
        self,
        query: str,
        domain: Optional[str] = None,
        sub_domain: Optional[str] = None,
        k: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieve relevant legal documents.
        
        Args:
            query: Search query
            domain: Legal domain filter
            sub_domain: Sub-domain for refined search
            k: Number of documents to retrieve
            
        Returns:
            Retrieved documents with metadata
        """
        try:
            # Build enhanced query
            enhanced_query = self._build_query(query, domain, sub_domain)
            
            # Retrieve from vector store
            documents = await self.vector_store.similarity_search(
                query=enhanced_query,
                k=k,
                filter_domain=domain,
                threshold=0.5
            )
            
            # Format results
            formatted_docs = self._format_documents(documents)
            
            logger.info(
                f"Retrieved {len(formatted_docs)} documents for query: {query[:50]}..."
            )
            
            return {
                "documents": formatted_docs,
                "query": enhanced_query,
                "count": len(formatted_docs),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Retrieval error: {str(e)}")
            return {
                "documents": [],
                "query": query,
                "count": 0,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _build_query(
        self,
        base_query: str,
        domain: Optional[str],
        sub_domain: Optional[str]
    ) -> str:
        """Build enhanced search query."""
        parts = [base_query]
        
        if domain:
            parts.append(domain)
        
        if sub_domain:
            parts.append(sub_domain)
        
        # Add procedure-focused terms
        parts.extend(["procedure", "process", "India"])
        
        return " ".join(parts)
    
    def _format_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format retrieved documents for response."""
        formatted = []
        
        for doc in documents:
            formatted.append({
                "id": doc.get("id", ""),
                "title": doc.get("act_name", "Legal Document"),
                "section": doc.get("section", ""),
                "chapter": doc.get("chapter", ""),
                "content": doc.get("content", ""),
                "source_url": doc.get("source_url", ""),
                "domain": doc.get("domain", ""),
                "relevance_score": doc.get("score", 0.0)
            })
        
        return formatted
    
    async def get_act_sections(
        self,
        act_name: str,
        section_numbers: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get specific sections from an act.
        
        Args:
            act_name: Name of the act
            section_numbers: List of section numbers
            
        Returns:
            List of section contents
        """
        try:
            sections = []
            
            for section in section_numbers:
                query = f"{act_name} section {section}"
                results = await self.vector_store.similarity_search(
                    query=query,
                    k=1,
                    threshold=0.7
                )
                
                if results:
                    sections.append(results[0])
            
            return sections
            
        except Exception as e:
            logger.error(f"Section retrieval error: {str(e)}")
            return []
    
    async def search_by_keywords(
        self,
        keywords: List[str],
        domain: Optional[str] = None,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search documents by keywords.
        
        Args:
            keywords: Search keywords
            domain: Optional domain filter
            k: Number of results
            
        Returns:
            Matching documents
        """
        query = " ".join(keywords)
        
        result = await self.retrieve(
            query=query,
            domain=domain,
            k=k
        )
        
        return result.get("documents", [])