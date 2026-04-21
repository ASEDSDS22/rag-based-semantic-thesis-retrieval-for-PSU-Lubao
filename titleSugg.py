import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import requests

# Load your dataset
df = pd.read_excel("thesis.xlsx")  # or thesis.csv
df.columns = df.columns.str.strip()  # Remove any leading/trailing whitespace from column names

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

def search(query):
    # Semantic search on full documents
    results = collection.query(
        query_embeddings=[model.encode(query).tolist()],
        n_results=5
    )
    
    # Also search for title matches
    title_matches = [text for text in texts if query.lower() in text.lower() and "title:" in text.lower()]
    
    # Combine results, with semantic results first
    combined_docs = results["documents"][0]
    for doc in title_matches:
        if doc not in combined_docs:
            combined_docs.append(doc)
    
    return [combined_docs[:5]]  # Return top 5 results

def suggest_titles(user_input):
    docs = search(user_input)
    context = "\n".join(docs[0])

    prompt = f"""Based on "{user_input}", suggest 5 thesis titles. Reply with ONLY the titles, no explanations or numbers:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3.5:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

if __name__ == "__main__":
    user_topic = input("Enter your research topic: ")
    print(suggest_titles(user_topic))
