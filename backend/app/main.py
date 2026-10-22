
from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Knowledge Assistant",
    description="Multi-tenant RAG application",
    version="0.1.0",
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
