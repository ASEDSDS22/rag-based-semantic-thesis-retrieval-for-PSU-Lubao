import chromadb

client = chromadb.Client()
collection = client.create_collection("test_db")

collection.add(
    documents=["Hello world"],
    embeddings=[[0.1, 0.2, 0.3]],
    ids=["1"]
)

print("Chroma working!")