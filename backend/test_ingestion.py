from backend.ingestion.pdf_ingest import extract_text_from_pdf
from backend.ingestion.image_ingest import ingest_image
from backend.ingestion.chunker import chunk_text
from backend.embeddings.text_embedder import TextEmbedder
from backend.retrieval.vector_store import VectorStore


# Load data
pdf_text = extract_text_from_pdf("data/uploads/sample.pdf")
image_text = ingest_image("data/uploads/sample.png")

combined_text = pdf_text + "\n" + image_text

# Chunk
chunks = chunk_text(combined_text)

# Embed
embedder = TextEmbedder()
embeddings = embedder.embed(chunks)

# Store
store = VectorStore(dim=embeddings.shape[1])
store.add(embeddings, chunks)

print(f"✅ Total chunks stored: {len(chunks)}")
