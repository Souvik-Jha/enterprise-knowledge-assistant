
from fastapi import FastAPI

from app.api.documents import router as documents_router

app = FastAPI(
    title="Enterprise Knowledge Assistant",
    description="Multi-tenant RAG application",
    version="0.1.0",
)

# Register document-related endpoints.
app.include_router(
    documents_router,
    prefix="/api/v1",
)

@app.get("/")
def root():
    return {
        "message": "Enterprise Knowledge Assistant API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
