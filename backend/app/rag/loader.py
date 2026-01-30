"""
Document Loader
Loads legal documents from various sources.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import re

from app.utils.logger import logger


class DocumentLoader:
    """
    Loads legal documents from various formats.
    Supports PDF, TXT, and DOCX files.
    """
    
    SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".docx", ".md"]
    
    def __init__(self):
        self.loaded_documents = []
    
    def load_directory(
        self,
        directory: str,
        recursive: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Load all documents from a directory.
        
        Args:
            directory: Path to directory
            recursive: Whether to search subdirectories
            
        Returns:
            List of loaded documents
        """
        documents = []
        path = Path(directory)
        
        if not path.exists():
            logger.error(f"Directory not found: {directory}")
            return documents
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in path.glob(pattern):
            if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    doc = self.load_file(str(file_path))
                    if doc:
                        documents.append(doc)
                except Exception as e:
                    logger.error(f"Error loading {file_path}: {str(e)}")
        
        logger.info(f"Loaded {len(documents)} documents from {directory}")
        return documents
    
    def load_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load a single document file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Document dictionary or None
        """
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return None
        
        extension = path.suffix.lower()
        
        if extension == ".pdf":
            return self._load_pdf(path)
        elif extension == ".txt":
            return self._load_txt(path)
        elif extension == ".docx":
            return self._load_docx(path)
        elif extension == ".md":
            return self._load_txt(path)  # Treat MD as text
        else:
            logger.warning(f"Unsupported file type: {extension}")
            return None
    
    def _load_pdf(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load PDF file."""
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(str(path))
            
            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            content = "\n\n".join(text_parts)
            
            return {
                "content": content,
                "source": str(path),
                "file_name": path.name,
                "file_type": "pdf",
                "metadata": self._extract_metadata_from_filename(path.name)
            }
            
        except Exception as e:
            logger.error(f"PDF load error: {str(e)}")
            return None
    
    def _load_txt(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load text file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            return {
                "content": content,
                "source": str(path),
                "file_name": path.name,
                "file_type": "txt",
                "metadata": self._extract_metadata_from_filename(path.name)
            }
            
        except Exception as e:
            logger.error(f"TXT load error: {str(e)}")
            return None
    
    def _load_docx(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load DOCX file."""
        try:
            from docx import Document
            
            doc = Document(str(path))
            
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            content = "\n\n".join(paragraphs)
            
            return {
                "content": content,
                "source": str(path),
                "file_name": path.name,
                "file_type": "docx",
                "metadata": self._extract_metadata_from_filename(path.name)
            }
            
        except Exception as e:
            logger.error(f"DOCX load error: {str(e)}")
            return None
    
    def _extract_metadata_from_filename(self, filename: str) -> Dict[str, Any]:
        """
        Extract metadata from filename.
        Expected format: ActName_Section_Chapter.ext
        """
        metadata: Dict[str, Any] = {
            "act_name": None,
            "section": None,
            "chapter": None,
            "domain": None
        }
        
        # Remove extension
        name = Path(filename).stem
        
        # Try to parse common patterns
        # Pattern: "IPC_Section_302" or "Consumer_Protection_Act_2019"
        parts = name.replace("-", "_").split("_")
        
        if parts:
            # Check for common act names
            act_indicators = ["act", "code", "ipc", "crpc", "cpc"]
            
            act_parts = []
            section = None
            chapter = None
            
            for i, part in enumerate(parts):
                if part.lower() in ["section", "sec", "s"]:
                    if i + 1 < len(parts):
                        section = parts[i + 1]
                elif part.lower() in ["chapter", "chap", "ch"]:
                    if i + 1 < len(parts):
                        chapter = parts[i + 1]
                elif part.lower() in act_indicators or i < 3:
                    act_parts.append(part)
            
            if act_parts:
                metadata["act_name"] = " ".join(act_parts)
            metadata["section"] = section
            metadata["chapter"] = chapter
        
        # Infer domain from act name
        metadata["domain"] = self._infer_domain(metadata.get("act_name", ""))
        
        return metadata
    
    def _infer_domain(self, act_name: Optional[str]) -> Optional[str]:
        """Infer legal domain from act name."""
        if not act_name:
            return None
        
        act_lower = act_name.lower()
        
        domain_keywords = {
            "Consumer Law": ["consumer", "trade", "commerce"],
            "Criminal Law": ["ipc", "penal", "criminal", "crpc", "crime"],
            "Labour Law": ["labour", "labor", "employment", "industrial", "wage", "factory"],
            "Family Law": ["marriage", "divorce", "hindu", "muslim", "christian", "adoption", "guardian"],
            "Property Law": ["property", "land", "registration", "transfer", "rent", "tenancy"],
            "Constitutional Law": ["constitution", "fundamental", "rti", "information"],
            "Civil Law": ["civil", "cpc", "contract", "specific relief", "limitation"]
        }
        
        for domain, keywords in domain_keywords.items():
            for keyword in keywords:
                if keyword in act_lower:
                    return domain
        
        return None
    
    def load_from_text(
        self,
        content: str,
        source: str = "manual",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a document from raw text.
        
        Args:
            content: Text content
            source: Source identifier
            metadata: Document metadata
            
        Returns:
            Document dictionary
        """
        return {
            "content": content,
            "source": source,
            "file_name": source,
            "file_type": "text",
            "metadata": metadata or {}
        }