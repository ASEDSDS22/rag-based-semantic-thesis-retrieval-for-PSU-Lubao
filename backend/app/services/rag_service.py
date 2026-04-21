"""RAG Service - Main business logic orchestration"""
from typing import List
from .retrieval import search
from .llm import llm_service
from ..utils.helpers import row_to_text


class RAGService:
    @staticmethod
    def query(question: str, top_k: int = 5) -> str:
        """
        Full RAG pipeline: retrieve + generate answer.
        Reused rag_answer() from data_loader.py
        """
        # Retrieve relevant docs
        docs = search(question, top_k)
        context = "\n\n".join(docs)
        
        prompt = f"""Answer the question using ONLY the context below. 
If you don't know the answer, say so.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

        answer = llm_service.generate(prompt)
        return answer
    
    @staticmethod
    def recommend_titles(topic: str, top_k: int = 5) -> str:
        """
        Recommend thesis titles based on topic.
        Reused suggest_titles() from titleSugg.py + recommend_topics() from data_loader.py
        """
        docs = search(topic, top_k)
        context = "\n\n".join(docs)
        
        prompt = f"""Based on the research topic "{topic}" and the following thesis examples:

{context}

Suggest 5 relevant thesis titles. Respond with ONLY the titles, numbered 1-5:"""

        titles = llm_service.generate(prompt)
        return titles


# Global service
rag_service = RAGService()
