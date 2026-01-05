from backend.ingestion.ocr import extract_text_from_image


def ingest_image(image_path: str) -> str:
    """
    Ingest image and extract text using OCR
    """
    text = extract_text_from_image(image_path)
    return text
