
from app.rag.chunker import chunk_pages


def test_chunking_preserves_source_and_page():
    pages = [
        {
            "text": "A" * 2500,
            "source": "sample.pdf",
            "page_number": 3,
        }
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=1000,
        overlap=200,
    )

    assert len(chunks) == 3
    assert chunks[0]["page_number"] == 3
    assert chunks[0]["source"] == "sample.pdf"
    assert chunks[1]["chunk_index"] == 1
    assert len(chunks[0]["content"]) == 1000
