"""Academia Sync - FastAPI Backend Entry Point"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .api.routes import router
from .core.config import settings
from .db.chroma_client import ChromaClient
from .services.embedding import embedding_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifespan: startup Chroma + embedding model"""
    # Startup
    print("🚀 Starting Academia Sync...")
    print(f"📚 ChromaDB: {settings.chroma_path}")
    print(f"🤖 LLM: {settings.model_name}")
    print(f"🔗 Embedding: {settings.embedding_model}")
    
    ChromaClient.get_collection()  # Init collection
    embedding_service.model  # Load model
    
    yield
    
    # Shutdown
    print("👋 Academia Sync shutdown")


app = FastAPI(
    title="Academia Sync 🎓",
    description="RAG-based Semantic Thesis Retrieval System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
