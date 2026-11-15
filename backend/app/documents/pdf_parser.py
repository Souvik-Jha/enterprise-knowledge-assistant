
from pathlib import Path

from pypdf import PdfReader


def extract_pages(pdf_path: str) -> list[dict]:
    """Extract text from a PDF while preserving page numbers."""
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    reader = PdfReader(str(path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        if text:
            pages.append({
                "page_number": page_number,
                "text": text,
                "source": path.name,
            })

    return pages
