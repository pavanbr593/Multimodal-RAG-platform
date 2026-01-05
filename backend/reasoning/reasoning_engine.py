from backend.reasoning.llm_engine import generate_answer
from backend.embeddings.text_embedder import TextEmbedder


class ReasoningEngine:
    def __init__(self, text_store, image_store):
        self.text_store = text_store
        self.image_store = image_store
        self.embedder = TextEmbedder()

    def answer(self, question: str):
        try:
            # 1️⃣ Embed question
            query_embedding = self.embedder.embed([question])[0]

            # 2️⃣ Retrieve context
            text_results = self.text_store.search(query_embedding, top_k=5)
            image_results = self.image_store.search(query_embedding, top_k=3)

            context = []

            for r in text_results:
                if isinstance(r, dict):
                    context.append(r.get("content", ""))
                elif isinstance(r, str):
                    context.append(r)

            prompt = f"""
You are an expert AI assistant.
Answer clearly and concisely using the context below.
If the context is insufficient, say so.

Context:
{chr(10).join(context)}

Question:
{question}

Answer:
"""

            # 3️⃣ LLM call
            answer_text = generate_answer(prompt)

            # 4️⃣ HARD GUARANTEED RESPONSE FORMAT
            return {
                "answer": answer_text if answer_text else "I couldn’t find enough information to answer this.",
                "confidence": 0.0,
                "sources": []
            }

        except Exception as e:
            # NEVER crash frontend again
            return {
                "answer": "An error occurred while generating the answer.",
                "confidence": 0.0,
                "sources": [],
                "error": str(e)
            }