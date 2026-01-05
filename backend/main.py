from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil


# -------------------- IMPORT PIPELINE MODULES --------------------
from backend.ingestion.pdf_ingest import extract_text_from_pdf
from backend.ingestion.image_ingest import extract_text_from_image
from backend.ingestion.chunker import chunk_text

from backend.embeddings.text_embedder import TextEmbedder
from backend.embeddings.image_embedder import ImageEmbedder

from backend.retrieval.vector_store import VectorStore
from backend.retrieval.multimodal_store import MultiModalStore

from backend.reasoning.reasoning_engine import ReasoningEngine

# -------------------- APP INIT --------------------
app = FastAPI(title="AI Knowledge Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------- GLOBAL OBJECTS --------------------
text_embedder = TextEmbedder()
image_embedder = None  # lazy load (important)
TEXT_EMBED_DIM = 384      # all-MiniLM-L6-v2
IMAGE_EMBED_DIM = 512     # CLIP

text_store = VectorStore(dim=TEXT_EMBED_DIM)
image_store = MultiModalStore(dim=IMAGE_EMBED_DIM)

reasoning_engine = ReasoningEngine(text_store, image_store)

# -------------------- SCHEMAS --------------------
class QueryRequest(BaseModel):
    question: str

# -------------------- ROUTES --------------------
@app.get("/")
def root():
    return {"status": "AI Knowledge Intelligence Platform running"}

# -------------------- UPLOAD --------------------
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    global image_embedder

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ext = file.filename.lower()

    # ---------- PDF ----------
    if ext.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text)

        embeddings = text_embedder.embed(chunks)
        text_store.add(embeddings, chunks)

        return {
            "status": "uploaded",
            "type": "pdf",
            "chunks_added": len(chunks)
        }

    # ---------- IMAGE ----------
    elif ext.endswith((".png", ".jpg", ".jpeg")):
        if image_embedder is None:
            image_embedder = ImageEmbedder()

        ocr_text = extract_text_from_image(file_path)
        image_embedding = image_embedder.embed(file_path)

        image_store.add(
            embeddings=[image_embedding],
            metadata=[{"path": file_path, "ocr": ocr_text}]
        )

        return {
            "status": "uploaded",
            "type": "image",
            "ocr_text_length": len(ocr_text)
        }

    return {"status": "unsupported file type"}

# -------------------- QUERY --------------------
@app.post("/query")
def query_docs(req: QueryRequest):
    try:
        result = reasoning_engine.answer(req.question)

        return {
            "answer": result.get("answer", ""),
            "confidence": result.get("confidence", 0.0),
            "sources": result.get("sources", [])
        }

    except Exception as e:
        return {
            "answer": "An error occurred while generating the answer.",
            "confidence": 0.0,
            "sources": [],
            "error": str(e)
        }
