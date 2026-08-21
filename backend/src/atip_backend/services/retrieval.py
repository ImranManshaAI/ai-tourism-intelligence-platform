from sentence_transformers import SentenceTransformer
from sqlalchemy import select
from sqlalchemy.orm import Session

from atip_backend.db.session import SessionLocal
from atip_backend.models.document_chunk import DocumentChunk
from atip_backend.schemas.retrieval import RetrievalResult


class RetrievalService:
    """Service responsible for semantic retrieval from the knowledge base."""

    MODEL_NAME = "BAAI/bge-m3"

    def __init__(self, db: Session | None = None) -> None:
        self.model = SentenceTransformer(self.MODEL_NAME)
        self.db = db or SessionLocal()

    def embed_query(self, query: str) -> list[float]:
        """Generate a normalized embedding for a search query."""
        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        """Search the knowledge base for relevant document chunks."""

        query_embedding = self.embed_query(query)

        distance = DocumentChunk.embedding.cosine_distance(query_embedding)

        statement = (
            select(
                DocumentChunk,
                (1 - distance).label("similarity"),
            )
            .where(DocumentChunk.embedding.is_not(None))
            .order_by(distance)
            .limit(top_k)
        )

        rows = self.db.execute(statement).all()

        return [
            RetrievalResult(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                content=chunk.content,
                page_number=chunk.page_number,
                similarity=float(similarity),
            )
            for chunk, similarity in rows
        ]
