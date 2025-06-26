# Updated chroma_sample.py for latest ChromaDB

import chromadb

# Use the new Client initialization method
client = chromadb.PersistentClient(path="./chroma_store")  # Creates/loads DB in this folder

# Create or get a collection
collection = client.get_or_create_collection(name="my_collection")

# Add some documents
collection.add(
    documents=[
        "The sky is blue.",
        "Deepfake videos are generated using GANs.",
        "Machine learning is a branch of AI.",
        "This document is about ChromaDB."
    ],
    ids=["doc1", "doc2", "doc3", "doc4"]
)

# Query the collection
results = collection.query(
    query_texts=["Tell me about deepfake"],
    n_results=2
)

# Display results
print("Query Results:")
print(results)
