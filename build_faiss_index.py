import json
import faiss
import os
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import pickle

# Paths
DATA_PATH = "flattened_constitution.jsonl"
INDEX_PATH = "faiss_index.index"
META_PATH = "index_metadata.pkl"

# Load your model
print("🔄 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, great for legal search

# Load the data
print("📄 Reading JSONL data...")
entries = []
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        entries.append(json.loads(line))

# Generate embeddings
print("🧠 Generating embeddings...")
texts = [entry["content"] for entry in entries]
embeddings = model.encode(texts, show_progress_bar=True)

# Create FAISS index
print("🧱 Creating FAISS index...")
dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index
print(f"💾 Saving index to {INDEX_PATH}")
faiss.write_index(index, INDEX_PATH)

# Save metadata for later use
print(f"💾 Saving metadata to {META_PATH}")
with open(META_PATH, 'wb') as f:
    pickle.dump(entries, f)

print(f"✅ Done! Indexed {len(entries)} constitutional entries.")
