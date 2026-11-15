# Enterprise Knowledge Assistant

A backend-focused, multi-tenant Retrieval-Augmented Generation (RAG) application that allows organizations to upload PDF documents and retrieve information through natural-language questions.

Built with Python, FastAPI, PostgreSQL, pgvector, SentenceTransformers, and OpenAI.

## Overview

Enterprise Knowledge Assistant processes company documents, converts their content into vector embeddings, and stores them in PostgreSQL using pgvector.

When a user asks a question, the application generates a query embedding, retrieves relevant document chunks using semantic similarity, and passes the retrieved context to an LLM to generate a grounded answer with source references.

## Architecture

```text
                 PDF Upload
                     |
                     v
               FastAPI Backend
                     |
                     v
                 PDF Parser
                     |
                     v
              Text Chunking
               (with overlap)
                     |
                     v
             SentenceTransformers
              (384D embeddings)
                     |
                     v
              PostgreSQL
                 pgvector
                     |
                     |
             Natural Language Query
                     |
                     v
              Query Embedding
                     |
                     v
              Semantic Retrieval
             (Company ID filter)
                     |
                     v
              Retrieved Chunks
                     |
                     v
                 OpenAI API
                     |
                     v
             Grounded Answer
              + Source Metadata
```

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Database | PostgreSQL 16 |
| Vector Search | pgvector |
| ORM | SQLAlchemy |
| Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |
| LLM | OpenAI GPT-4o-mini |
| PDF Processing | pypdf |
| Containerization | Docker, Docker Compose |

## Implemented Features

### 1. Document Ingestion
- PDF upload through FastAPI.
- PDF text extraction using pypdf.
- File size and basic PDF validation.
- Temporary file handling and cleanup.

### 2. Text Chunking
- Splits extracted document text into smaller chunks.
- Configurable chunk size and overlap.
- Preserves page numbers and chunk metadata.

### 3. Embedding Generation
- Uses SentenceTransformers with `all-MiniLM-L6-v2`.
- Generates 384-dimensional embeddings.
- Uses the same embedding model for documents and user queries.
- Normalizes embeddings before storage and retrieval.

### 4. Vector Storage
- PostgreSQL with the pgvector extension.
- Stores document chunks, embeddings, and metadata.
- Uses relational document and company references.

### 5. Semantic Search
- Converts natural-language questions into embeddings.
- Retrieves relevant chunks using cosine distance.
- Filters retrieval results by company ID.
- Supports configurable top-k retrieval and an experimental distance threshold.

### 6. LLM Integration
- Integrates OpenAI GPT-4o-mini.
- Constructs prompts using retrieved document context.
- Generates answers grounded in retrieved content.
- Instructs the model to acknowledge when information is unavailable.

### 7. Source Attribution
- Associates retrieved chunks with their original document.
- Returns document filename, page number, chunk index, and retrieval distance.
- Includes source identifiers in generated answers.

## Project Structure

```text
enterprise-knowledge-assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── documents.py
│   │   ├── core/
│   │   ├── database/
│   │   │   ├── database.py
│   │   │   └── models/
│   │   ├── documents/
│   │   │   ├── pdf_parser.py
│   │   │   └── ingestion_service.py
│   │   ├── rag/
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── retriever.py
│   │   │   └── generator.py
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── docs/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12
- Docker and Docker Compose
- OpenAI API key

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd enterprise-knowledge-assistant
```

### 2. Start PostgreSQL with pgvector

```bash
docker compose up -d
```

The database container uses PostgreSQL 16 with pgvector.

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://eka_user:eka_local_password@localhost:5432/enterprise_knowledge
OPENAI_API_KEY=your_openai_api_key
```

Never commit your actual `.env` file or API keys.

### 4. Set up the Python environment

```bash
cd backend

python3.12 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### 5. Initialize the database

Ensure the pgvector extension and the required application tables are created.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

The current implementation uses manually created database tables. Database migrations are planned for a future improvement.

### 6. Run the application

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API documentation is available at:

```text
http://localhost:8000/docs
```

## API Endpoints

### Upload a document

```http
POST /api/v1/documents/upload
```

Multipart form data:

| Field | Type |
|---|---|
| file | PDF file |
| company_id | UUID |

Example:

```bash
curl -X POST \
  "http://localhost:8000/api/v1/documents/upload" \
  -F "company_id=YOUR_COMPANY_UUID" \
  -F "file=@./sample.pdf"
```

The endpoint processes the document, generates embeddings, and stores its chunks in PostgreSQL.

### Query documents

```http
POST /api/v1/documents/query
```

Query parameters:

| Parameter | Type |
|---|---|
| query | String |
| company_id | UUID |

Example:

```bash
curl -X POST \
  "http://localhost:8000/api/v1/documents/query?query=What%20is%20the%20document%20about%3F&company_id=YOUR_COMPANY_UUID"
```

The endpoint generates a query embedding, retrieves relevant document chunks, and generates an answer using OpenAI.

## Current Limitations

This is an actively developed backend MVP, not yet a production-ready enterprise deployment.

- Authentication and authorization are not implemented.
- Company ID is currently supplied by the API caller; it must be derived from authenticated identity before production use.
- Automated retrieval and answer evaluation are still being developed.
- Citation marker validation requires further hardening.
- Database migrations are not yet implemented.
- Only text-extractable PDFs are supported; OCR for scanned documents is not implemented.
- Retrieval currently uses vector similarity search without reranking or hybrid search.
- Deployment and production monitoring are pending.

## Planned Improvements

- Authentication and role-based access control.
- Automated RAG evaluation.
- Citation validation and answer-quality improvements.
- Hybrid search combining keyword and semantic retrieval.
- Reranking retrieved chunks.
- HNSW vector indexing.
- Redis caching.
- Conversation history and chat management.
- Production deployment and monitoring.

## Learning Objectives

This project is also an implementation-focused exploration of AI Engineering concepts:

- Retrieval-Augmented Generation (RAG).
- Text chunking strategies.
- Dense embeddings and semantic search.
- Vector databases and pgvector.
- LLM prompt engineering.
- Context construction and source attribution.
- Multi-tenant data isolation.
- Backend architecture for LLM-powered applications.

---

**Status:** Backend MVP — core document ingestion, semantic retrieval, and LLM answer generation implemented.

**Note:** This project is under active development. Features listed under Planned Improvements are not yet implemented.
