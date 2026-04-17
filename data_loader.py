import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

# Load your dataset
df = pd.read_excel("thesis.xlsx")  # or thesis.csv
df.columns = df.columns.str.strip()  # Remove any leading/trailing whitespace from column names

print(df.head())

def row_to_text(row):
    
    return f"""
    Title: {row['title_clean']}
    Journal: {row['journal_clean']}
    Year: {row['year']}
    Authors: {row['authors']}
    Keywords: {row['keyword']}
    """

texts = []

for _, row in df.iterrows():
    texts.append(row_to_text(row))

print("\nSample text:\n", texts[0])

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection("thesis_db")

for i, text in enumerate(texts):
    embedding = model.encode(text).tolist()

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(i)]
    )

print("\nData stored in Chroma!")

def search(query):
    results = collection.query(
        query_embeddings=[model.encode(query).tolist()],
        n_results=3
    )
    return results["documents"]

print("\nSearch Results:")
print(search("machine learning"))

import requests

def rag_answer(query):
    docs = search(query)
    context = "\n".join(docs[0])

    prompt = f"""
    Answer the question using ONLY the context below:

    {context}

    Question: {query}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3.5:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

    

print("\nAI Answer:")
print(rag_answer("What are common machine learning research topics?"))

print(rag_answer("What are common machine learning research topics?"))