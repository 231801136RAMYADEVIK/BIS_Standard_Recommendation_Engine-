import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
CACHE = "data/embeddings_cache.pkl"

def build_index(chunks: list[dict]) -> tuple:
    texts = [c["text"] for c in chunks]
    standard_ids = [c.get("standard_id", "UNKNOWN") for c in chunks]

    if os.path.exists(CACHE):
        print("Loading cached embeddings...")
        with open(CACHE, "rb") as f:
            embeddings = pickle.load(f)
    else:
        print("Encoding embeddings...")
        embeddings = model.encode(texts, batch_size=64, show_progress_bar=True)
        embeddings = np.array(embeddings).astype('float32')
        with open(CACHE, "wb") as f:
            pickle.dump(embeddings, f)
        print(f"Cached {len(embeddings)} embeddings")

    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index, texts, embeddings, standard_ids