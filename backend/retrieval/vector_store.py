import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings, metadatas):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)

        for m in metadatas:
            # ✅ HARD SAFETY
            if isinstance(m, dict):
                self.metadata.append(m)
            else:
                self.metadata.append({"content": str(m), "source": "unknown"})

    def search(self, query_vector, top_k=5):
        query = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results