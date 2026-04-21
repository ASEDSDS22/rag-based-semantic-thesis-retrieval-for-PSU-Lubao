"""Embedding service using sentence-transformers"""
from sentence_transformers import SentenceTransformer
from ..core.config import settings
from typing import List


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)
    
    def encode(self, texts: List[str]) -> List[list]:
        """
        Generate embeddings for texts.
        Reused from original data_loader.py/titleSugg.py
        """
        embeddings = self.model.encode(texts)
        return embeddings.tolist()


# Global instance
embedding_service = EmbeddingService()
