"""ChromaDB Client for Academia Sync"""
import chromadb
from chromadb.config import Settings
from ..core.config import settings


class ChromaClient:
    _client = None
    _collection = None
    
    @classmethod
    def get_client(cls):
        """Get persistent Chroma client"""
        if cls._client is None:
            cls._client = chromadb.PersistentClient(
                path=settings.chroma_path,
                settings=Settings(anonymized_telemetry=False)
            )
        return cls._client
    
    @classmethod
    def get_collection(cls, name: str = None):
        """Get or create thesis collection"""
        if name is None:
            name = settings.chroma_collection
            
        client = cls.get_client()
        try:
            cls._collection = client.get_collection(name)
        except:
            cls._collection = client.create_collection(name)
            
        return cls._collection


# Global access
chroma_client = ChromaClient.get_client()
thesis_collection = ChromaClient.get_collection()
