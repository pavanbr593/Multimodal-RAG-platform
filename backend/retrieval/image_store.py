import faiss
import numpy as np


class ImageVectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings, meta):
        self.index.add(np.array(embeddings).astype("float32"))
        self.metadata.extend(meta)

    def search(self, query_embedding, top_k=3):
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"), top_k
        )
        return [self.metadata[i] for i in indices[0]]