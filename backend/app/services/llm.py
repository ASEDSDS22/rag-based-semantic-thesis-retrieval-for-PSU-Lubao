"""LLM Service using Ollama"""
import requests
import ollama
from ..core.config import settings
from typing import Optional


class LLMService:
    def __init__(self):
        self.model = settings.model_name
        self.base_url = settings.ollama_base_url
    
    def generate(self, prompt: str, stream: bool = False) -> str:
        """
        Generate response from Ollama.
        Supports both requests API and ollama lib (fallback).
        Reused from data_loader.py/titleSugg.py/chatbot.py
        """
        try:
            # Try ollama lib first (chatbot.py style)
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                stream=stream
            )
            return response['response']
        except:
            # Fallback to requests API (original scripts)
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": stream
                },
                timeout=60
            )
            resp.raise_for_status()
            return resp.json()["response"]


llm_service = LLMService()
