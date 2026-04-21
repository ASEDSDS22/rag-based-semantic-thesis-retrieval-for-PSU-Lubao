"""Academia Sync - Configuration Settings"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # LLM
    model_name: str = "phi3.5:latest"
    ollama_base_url: str = "http://localhost:11434"
    
    # Embedding
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # ChromaDB
    chroma_path: str = "./chroma_db"
    chroma_collection: str = "thesis_db"
    
    # Data
    thesis_data_path: str = "../data/thesis.xlsx"
    
    # API
    api_v1_str: str = "/api/v1"
    
    # Development
    debug: bool = True
    
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
