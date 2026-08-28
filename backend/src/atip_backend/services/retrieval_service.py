from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from atip_backend.models.document_chunk import DocumentChunk
from atip_backend.services.embedding_service import EmbeddingService


class RetrievalService:
    """Retrieve relevant document chunks using vector similarity."""

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

    def search(
        self,
        db: Session,
        query: str,
        document_id: UUID | None = None,
        limit: int = 5,
    ) -> list[dict]:
        """Return the most relevant chunks for a query."""

        if not query.strip():
            raise ValueError(
                "Query cannot be empty"
            )

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than zero"
            )

        query_embedding = self.embedding_service.embed_text(
            query
        )

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        ).label("distance")

        statement = (
            select(
                DocumentChunk,
                distance,
            )
            .where(
                DocumentChunk.embedding.is_not(None)
            )
            .order_by(distance)
            .limit(limit)
        )

        if document_id is not None:
            statement = statement.where(
                DocumentChunk.document_id == document_id
            )

        results = db.execute(statement).all()

        return [
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "page_number": chunk.page_number,
                "similarity": 1 - float(distance),
            }
            for chunk, distance in results
        ]
