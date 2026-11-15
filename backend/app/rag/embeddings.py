from sentence_transformers import SentenceTransformer
from uuid import UUID
from app.rag.retriever import search_similar_chunks

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")



    def embed_chunks(self,chunks: list[dict])-> list[dict]:
        if not chunks:
            return []
        texts = [chunk["content"] for chunk in chunks]
        vectors = self.model.encode(texts,normalize_embeddings=True).tolist()
        for chunk, vector in zip(chunks, vectors):
            chunk["embedding"]= vector
        return chunks
    

    def embed_query(self,query_str: str)-> list[float]:
        if not query_str or not query_str.strip():
            raise ValueError("Query cannot be empty.")
        vectors = self.model.encode(query_str,normalize_embeddings=True).tolist()
        
        return vectors


        

