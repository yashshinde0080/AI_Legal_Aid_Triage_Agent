"""
Text Chunker
Splits documents into chunks for embedding.
"""

from typing import List, Dict, Any, Optional
import re

from app.utils.logger import logger


class TextChunker:
    """
    Splits documents into chunks for embedding and retrieval.
    Uses semantic boundaries when possible.
    """
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        min_chunk_size: int = 100
    ):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Target size for chunks (in characters)
            chunk_overlap: Overlap between chunks
            min_chunk_size: Minimum chunk size
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def chunk_document(
        self,
        document: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Chunk a document.
        
        Args:
            document: Document with content and metadata
            
        Returns:
            List of chunk dictionaries
        """
        content = document.get("content", "")
        metadata = document.get("metadata", {})
        source = document.get("source", "unknown")
        
        if not content:
            return []
        
        # Try section-based chunking first for legal documents
        chunks = self._chunk_by_sections(content)
        
        if not chunks:
            # Fall back to character-based chunking
            chunks = self._chunk_by_characters(content)
        
        # Create chunk documents
        chunk_docs = []
        for i, chunk_text in enumerate(chunks):
            if len(chunk_text.strip()) < self.min_chunk_size:
                continue
            
            chunk_doc = {
                "content": chunk_text.strip(),
                "source": source,
                "chunk_index": i,
                "total_chunks": len(chunks),
                **metadata
            }
            chunk_docs.append(chunk_doc)
        
        logger.info(f"Created {len(chunk_docs)} chunks from {source}")
        return chunk_docs
    
    def _chunk_by_sections(self, text: str) -> List[str]:
        """
        Chunk text by section markers.
        Looks for patterns like "Section 1", "CHAPTER I", etc.
        """
        # Patterns for legal section markers
        section_patterns = [
            r'\n(?=Section\s+\d+)',
            r'\n(?=SECTION\s+\d+)',
            r'\n(?=CHAPTER\s+[IVXLCDM]+)',
            r'\n(?=Chapter\s+\d+)',
            r'\n(?=Article\s+\d+)',
            r'\n(?=ARTICLE\s+\d+)',
            r'\n(?=Part\s+[IVXLCDM]+)',
            r'\n(?=PART\s+[IVXLCDM]+)',
        ]
        
        chunks = []
        current_text = text
        
        for pattern in section_patterns:
            parts = re.split(pattern, current_text)
            if len(parts) > 1:
                for part in parts:
                    if len(part.strip()) > self.min_chunk_size:
                        # If part is too large, chunk it further
                        if len(part) > self.chunk_size * 2:
                            chunks.extend(self._chunk_by_characters(part))
                        else:
                            chunks.append(part)
                return chunks
        
        return []
    
    def _chunk_by_characters(self, text: str) -> List[str]:
        """
        Chunk text by character count with overlap.
        Tries to break at sentence or paragraph boundaries.
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Find end position
            end = start + self.chunk_size
            
            if end >= text_length:
                # Last chunk
                chunk = text[start:].strip()
                if len(chunk) >= self.min_chunk_size:
                    chunks.append(chunk)
                break
            
            # Try to find a good break point
            break_point = self._find_break_point(text, start, end)
            
            chunk = text[start:break_point].strip()
            if len(chunk) >= self.min_chunk_size:
                chunks.append(chunk)
            
            # Move start with overlap
            start = break_point - self.chunk_overlap
            if start < 0:
                start = break_point
        
        return chunks
    
    def _find_break_point(self, text: str, start: int, end: int) -> int:
        """
        Find a good break point near the end position.
        Prefers paragraph > sentence > word boundaries.
        """
        search_start = max(start, end - 200)
        search_text = text[search_start:end + 100]
        
        # Try to find paragraph break
        para_match = re.search(r'\n\n', search_text)
        if para_match:
            return search_start + para_match.end()
        
        # Try to find sentence break
        sentence_match = re.search(r'[.!?]\s+', search_text)
        if sentence_match:
            return search_start + sentence_match.end()
        
        # Try to find word break
        word_match = re.search(r'\s+', search_text[::-1])
        if word_match:
            return end - word_match.start()
        
        return end
    
    def chunk_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Chunk multiple documents.
        
        Args:
            documents: List of documents
            
        Returns:
            List of all chunks
        """
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        
        logger.info(f"Created {len(all_chunks)} total chunks from {len(documents)} documents")
        return all_chunks