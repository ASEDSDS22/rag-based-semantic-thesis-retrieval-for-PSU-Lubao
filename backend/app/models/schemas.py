"""Pydantic models for API requests/responses"""
from pydantic import BaseModel, Field
from typing import Optional, List


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User question")
    top_k: Optional[int] = Field(5, ge=1, le=20)


class AnswerResponse(BaseModel):
    answer: str
    context_docs: Optional[List[str]] = None


class TitleRequest(BaseModel):
    topic: str = Field(..., min_length=1, description="Research topic/abstract")
    top_k: Optional[int] = Field(5, ge=1, le=20)


class TitlesResponse(BaseModel):
    titles: str
    context_docs: Optional[List[str]] = None


class IngestResponse(BaseModel):
    status: str = "success"
    ingested_count: Optional[int] = None
    message: Optional[str] = None


class HealthResponse(BaseModel):
    status: str = "healthy"
    chroma_ready: bool
    services: dict
