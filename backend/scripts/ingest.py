"""Standalone thesis ingestion script"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.db.chroma_client import ChromaClient
from app.services.embedding import embedding_service
from app.utils.helpers import row_to_text
import pandas


def main():
    """Ingest theses from Excel to ChromaDB"""
    print("🚀 Academia Sync - Ingestion Script")
    
    df = pandas.read_excel(settings.thesis_data_path)
    df.columns = df.columns.str.strip()
    
    texts = []
    collection = ChromaClient.get_collection()
    existing_count = collection.count()
    
    print(f"📊 Found {len(df)} theses in {settings.thesis_data_path}")
    
    for i, (_, row) in enumerate(df.iterrows()):
        text = row_to_text(row.to_dict())
        if text not in texts:
            texts.append(text)
    
    if texts:
        embeddings = embedding_service.encode(texts)
        collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=[f"doc_{existing_count + i}" for i in range(len(texts))]
        )
        print(f"✅ Ingested {len(texts)} unique theses. Total: {collection.count()}")
    else:
        print("ℹ️ No new theses to ingest")


if __name__ == "__main__":
    main()
