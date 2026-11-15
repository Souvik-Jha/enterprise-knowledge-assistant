from app.database.models import Document, DocumentChunk
from uuid import UUID
from sqlalchemy.orm import Session


def ingest_document(
    db: Session,
    filename: str,
    chunks: list[dict],
    company_id: UUID,
):
    try:
        # 1. Create a Python object
        document = Document(filename=filename, company_id=company_id, status='uploaded')

        # 2. Add the object to the session
        db.add(document)

        # Send the INSERT to PostgreSQL and get the generated document ID.
        # The transaction is still not committed.
        db.flush()

        document_chunks = []

        for chunk in chunks:
            document_chunk = DocumentChunk(
                document_id=document.id,
                company_id=company_id,
                content=chunk["content"],
                embedding=chunk["embedding"],
                page_number=chunk["page_number"],
                chunk_index=chunk["chunk_index"],
            )

            document_chunks.append(document_chunk)

        # 3. Add all chunk records to the session.
        db.add_all(document_chunks)

        # 4. Update the document status.
        document.status = "processed"

        # 3. Save the transaction in PostgreSQL
        db.commit()

        return {
            "document_id": str(document.id),
            "filename": document.filename,
            "status": document.status,
            "total_chunks": len(document_chunks),
        }

    except Exception:
        # Undo the transaction if something fails
        db.rollback()
        raise

    