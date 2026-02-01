from typing import List, Dict, Any
from app.utils.logger import logger
import asyncio

class DocumentEmbedder:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        batch_size: int = 32,
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self._model = None
    
    @property
    def model(self):
        """Lazy load the model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                logger.error("sentence-transformers not installed. Please run: pip install sentence-transformers")
                raise
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise
        return self._model

    async def embed_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Embed documents using local SentenceTransformer model.
        Runs in a thread pool to avoid blocking the event loop.
        """
        if not documents:
            return []

        texts = [d.get("content", "") for d in documents]

        logger.info(f"Embedding {len(texts)} documents locally")

        # Run model.encode in a thread pool since it's CPU bound
        loop = asyncio.get_running_loop()
        embeddings = await loop.run_in_executor(
            None,
            lambda: self.model.encode(
                texts,
                batch_size=self.batch_size,
                show_progress_bar=True,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
        )

        embedded_docs = []
        for doc, emb in zip(documents, embeddings):
            doc["embedding"] = emb.tolist()
            embedded_docs.append(doc)

        return embedded_docs

    def embed_documents_sync(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Synchronous wrapper for embedding documents."""
        if not documents:
            return []
            
        texts = [d.get("content", "") for d in documents]
        
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        
        embedded_docs = []
        for doc, emb in zip(documents, embeddings):
            doc["embedding"] = emb.tolist()
            embedded_docs.append(doc)
            
        return embedded_docs