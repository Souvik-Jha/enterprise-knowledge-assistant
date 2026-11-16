             DOCUMENT INGESTION

PDF Upload
    |
PDF Parser
    |
Text Extraction
    |
Chunking
    |
Embedding Model
    |
PostgreSQL + pgvector


              QUERY PIPELINE

User Question
    |
Query Embedding
    |
Vector Similarity Search
    |
Top-K Retrieved Chunks
    |
LLM + System Prompt
    |
Grounded Answer + Sources