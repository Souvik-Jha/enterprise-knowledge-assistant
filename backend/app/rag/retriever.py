from sqlalchemy import select
from uuid import UUID
from sqlalchemy.orm import Session

from app.database.models import Document,DocumentChunk


def search_similar_chunks(
    db: Session,
    company_id: UUID,
    query_embedding: list[float],
    top_k : int = 5,
    max_distance: float = 0.75
):
    if not query_embedding:
        raise ValueError("Query embedding cannot be empty.")

    if len(query_embedding) != 384:
        raise ValueError("Query embedding must have 384 dimensions.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    distance = DocumentChunk.embedding.cosine_distance(query_embedding)
    statement = (
        select(
            DocumentChunk,
            Document.filename,
            distance.label("distance"),
        )
        .join(
            Document,
            (Document.id == DocumentChunk.document_id)
            & (Document.company_id == DocumentChunk.company_id),
        )
        .where(DocumentChunk.company_id == company_id)
        .where(distance <= max_distance)
        .order_by(distance.asc())
        .limit(top_k)
    )
    results = db.execute(statement).all()

    return results