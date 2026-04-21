import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
import re

# Load dataset
df = pd.read_excel("thesis.xlsx")
df.columns = df.columns.str.strip()

def parse_text_to_dict(text):
    """Parse thesis text back to dict for citation."""
    title = re.search(r'Title: (.*)', text).group(1).strip()
    journal = re.search(r'Journal: (.*)', text).group(1).strip() if re.search(r'Journal: (.*)', text) else ''
    year = re.search(r'Year: (.*)', text).group(1).strip()
    authors = re.search(r'Authors: (.*)', text).group(1).strip()
    return {'title': title, 'journal': journal, 'year': year, 'authors': authors}

# Model and Chroma setup (reuse existing)
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client(Settings(persist_directory="./chroma_db"))
try:
    collection = client.get_collection("thesis_db")
except:
    # Fallback create if not exists (from other scripts)
    texts = [row_to_text(row) for _, row in df.iterrows()]
    embeddings = model.encode(texts).tolist()
    collection = client.create_collection("thesis_db")
    collection.add(documents=texts, embeddings=embeddings, ids=[str(i) for i in range(len(texts))])

def row_to_text(row):
    return f"""
Title: {row['title_clean']}
Journal: {row['journal_clean']}
Year: {row['year']}
Authors: {row['authors']}
Keywords: {row['keyword']}
"""

def semantic_search(query, n_results=5):
    results = collection.query(
        query_embeddings=[model.encode(query).tolist()],
        n_results=n_results
    )
    return results["documents"][0], results["ids"][0]

def generate_apa_citation(thesis_text):
    """Generate APA style citation."""
    data = parse_text_to_dict(thesis_text)
    authors = data['authors']
    year = data['year']
    title = data['title']
    journal = data['journal']
    
    # Simple APA: Lastname, F. M. et al. (Year). Title. Journal.
    citation = f"{authors}. ({year}). {title}. {journal}."
    return citation.strip()

if __name__ == "__main__":
    print("Citation Generator (Ctrl+C to exit)")
    while True:
        try:
            query = input("\nEnter topic/query for search (or 'quit'): ").strip()
            if query.lower() == 'quit':
                break
            if not query:
                continue
            
            docs, ids = semantic_search(query)
            print("\nTop matching theses:")
            for i, doc in enumerate(docs):
                data = parse_text_to_dict(doc)
                print(f"{i+1}. {data['authors']} ({data['year']}). {data['title'][:80]}...")
            
            choice = input("Select number for citation (1-5) or new search: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(docs):
                selected = docs[int(choice)-1]
                citation = generate_apa_citation(selected)
                print(f"\nAPA Citation:\n{citation}")
            else:
                print("Invalid, try again.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
``