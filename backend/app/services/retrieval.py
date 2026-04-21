"""Vector retrieval service"""
from typing import List
from ..db.chroma_client import thesis_collection
from .embedding import embedding_service


def search(query: str, n_results: int = 5) -> List[str]:
    """
    Semantic search in thesis collection.
    Reused from data_loader.py/titleSugg.py search()
    """
    query_embedding = embedding_service.encode([query])[0]
    
    results = thesis_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results["documents"][0]


__all__ = ["search"]
