from sentence_transformers import SentenceTransformer


class TextEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts: list):
        return self.model.encode(texts)
