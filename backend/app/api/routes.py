"""API Routes for Academia Sync"""
from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import (
    QueryRequest, AnswerResponse, TitleRequest, TitlesResponse, 
    IngestResponse, HealthResponse
)
from ..services.rag_service import rag_service
from ..services.retrieval import search
from ..services.embedding import embedding_service
from ..db.chroma_client import thesis_collection
from ..core.config import settings
import pandas
from typing import List
from ..utils.helpers import row_to_text


router = APIRouter(prefix="/api/v1", tags=["academia-sync"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        chroma_ready=bool(thesis_collection.count()),
        services={
            "embedding": "ready",
            "llm": settings.model_name,
            "rag": "ready"
        }
    )


@router.post("/query", response_model=AnswerResponse)
async def query_theses(request: QueryRequest):
    """Semantic search + RAG answer"""
    try:
        docs = search(request.query, request.top_k)
        answer = rag_service.query(request.query, request.top_k)
        
        return AnswerResponse(
            answer=answer,
            context_docs=docs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend-title", response_model=TitlesResponse)
async def recommend_title(request: TitleRequest):
    """AI-generated thesis title suggestions"""
    try:
        docs = search(request.topic, request.top_k)
        titles = rag_service.recommend_titles(request.topic, request.top_k)
        
        return TitlesResponse(
            titles=titles,
            context_docs=docs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest", response_model=IngestResponse)
async def ingest_theses():
    """Ingest thesis data from Excel (idempotent)"""
    try:
        df = read_excel(settings.thesis_data_path)
        df.columns = df.columns.str.strip()
        
        texts = []
        existing_count = thesis_collection.count()
        
        for _, row in df.iterrows():
            text = row_to_text(row.to_dict())
            if text not in texts:  # Dedupe
                texts.append(text)
        
        if texts:
            embeddings = embedding_service.encode(texts)
            thesis_collection.add(
                documents=texts,
                embeddings=embeddings,
                ids=[f"doc_{existing_count + i}" for i in range(len(texts))]
            )
        
        return IngestResponse(
            ingested_count=len(texts),
            message=f"Ingested {len(texts)} theses. Total: {thesis_collection.count()}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
