
import tempfile
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, Form
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.documents.pdf_parser import extract_pages
from app.rag.chunker import chunk_pages
from app.documents.ingestion_service import ingest_document
from app.rag.retriever import search_similar_chunks
from app.rag.generator import generate_ans
from app.rag.embeddings import EmbeddingService


Embedding_service = EmbeddingService()


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/upload")
async def preview_document(
    file: UploadFile = File(...),
    company_id: UUID = Form(...),
    db: Session = Depends(get_db),
):
    # 1. Validate the filename.
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    # 2. Read the uploaded file and enforce a size limit.
    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB.",
        )

    # 3. Check the PDF signature. This is an initial check;
    # the PDF parser must still validate the file.
    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file does not appear to be a PDF.",
        )

    temp_path = None

    try:
        # 4. Save the uploaded bytes to a temporary PDF file.
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        # 5. Reuse our existing PDF parser.
        pages = extract_pages(temp_path)

        # 6. Reject PDFs with no extractable text.
        if not pages:
            raise HTTPException(
                status_code=422,
                detail="No extractable text was found in the PDF.",
            )

        # 7. Reuse our existing chunker.
        chunks = chunk_pages(pages)
        chunks_with_embeddings =Embedding_service.embed_chunks(chunks)
        result = ingest_document(
            db=db,
            filename=Path(file.filename).name,
            chunks=chunks_with_embeddings,
            company_id=company_id,
        )

        # 8. Return the result as JSON.
        return {
            **result,
            "total_pages": len(PdfReader(temp_path).pages),
        }

    except HTTPException:
        raise

    except (PdfReadError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail="The PDF is invalid or could not be processed.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the PDF.",
        ) from exc

    finally:
        # 9. Always clean up the temporary file.
        if temp_path and Path(temp_path).exists():
            Path(temp_path).unlink()

        await file.close()



@router.post("/query")
async def retrieve_answer(
    quert_str:  str,
    company_id: UUID,
    db: Session = Depends(get_db),

):
    if not quert_str :
        raise HTTPException(
            status_code=400,
            detail="Ask a valid question",
        )
    try:
        query_embedding =Embedding_service.embed_query(quert_str)
        retrival = search_similar_chunks(db=db,company_id=company_id,query_embedding=query_embedding,top_k=5,max_distance=0.75 )
        grounded_ans = generate_ans(quert_str,retrival)
        return grounded_ans

    except HTTPException:
        raise

     

