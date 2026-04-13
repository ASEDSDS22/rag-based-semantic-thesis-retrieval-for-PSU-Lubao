from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Hello RAG system"
vector = model.encode(text)

print("Embedding size:", len(vector))