from backend.ingestion.pdf_ingest import extract_text_from_pdf
from backend.ingestion.image_ingest import ingest_image
from backend.ingestion.chunker import chunk_text

from backend.embeddings.text_embedder import TextEmbedder
from backend.embeddings.image_embedder import ImageEmbedder

from backend.retrieval.text_store import TextVectorStore
from backend.retrieval.image_store import ImageVectorStore


# -------- LOAD DATA --------
pdf_path = "data/uploads/sample.pdf"
image_path = "data/uploads/sample.png"

pdf_text = extract_text_from_pdf(pdf_path)
image_text = ingest_image(image_path)

chunks = chunk_text(pdf_text + "\n" + image_text)

# -------- EMBEDDINGS --------
text_embedder = TextEmbedder()
text_embeddings = text_embedder.embed(chunks)

image_embedder = ImageEmbedder()
image_embeddings = image_embedder.embed([image_path])

# -------- VECTOR STORES --------
text_store = TextVectorStore(dim=text_embeddings.shape[1])
image_store = ImageVectorStore(dim=image_embeddings.shape[1])

# Add text
text_meta = [
    {"type": "text", "content": c, "source": "sample.pdf"}
    for c in chunks
]
text_store.add(text_embeddings, text_meta)

# Add image
image_meta = [
    {"type": "image", "path": image_path}
]
image_store.add(image_embeddings, image_meta)

print(f"✅ Stored {len(text_meta)} text chunks + {len(image_meta)} image")

# -------- QUERY --------
query = "What disease symptoms are described?"
query_embedding = text_embedder.embed([query])[0]

text_results = text_store.search(query_embedding)
image_results = image_store.search(image_embeddings[0])

print("\n🔍 TEXT RESULTS:\n")
for r in text_results:
    print(r)
    print("-" * 40)

print("\n🖼️ IMAGE RESULTS:\n")
for r in image_results:
    print(r)
    print("-" * 40)
