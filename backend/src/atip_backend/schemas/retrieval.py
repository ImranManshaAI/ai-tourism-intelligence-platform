from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RetrievalResult(BaseModel):
    """A document chunk returned by semantic retrieval."""

    model_config = ConfigDict(from_attributes=True)

    chunk_id: UUID
    document_id: UUID
    content: str
    page_number: int | None
    similarity: float
