from backend.embeddings.text_embedder import TextEmbedder
from backend.retrieval.text_store import TextVectorStore
from backend.retrieval.image_store import ImageVectorStore
from backend.reasoning.prompts import build_prompt
from backend.reasoning.llm_engine import generate_answer
from backend.reasoning.confidence import compute_confidence

# Dummy retrieval results (reuse from Phase 2 output manually)
text_chunks = [
    "Vector-borne diseases increase due to warmer climates...",
    "Environmental changes affect disease spread patterns..."
]

image_descriptions = [
    "Leaf image shows dark spots and yellowing edges"
]

question = "What disease symptoms are shown and what are the causes?"

prompt = build_prompt(question, text_chunks, image_descriptions)
answer = generate_answer(prompt)

confidence = compute_confidence(len(text_chunks) + len(image_descriptions))

print("\n🧠 ANSWER:\n")
print(answer)

print("\n📌 CONFIDENCE:", confidence)
print("\n📚 SOURCES USED:", len(text_chunks) + len(image_descriptions))
