from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """Public representation of an uploaded document."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    filename: str
    original_filename: str
    content_type: str
    file_size: int
    status: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class DocumentProcessResponse(BaseModel):
    """Result of document processing."""

    document_id: UUID
    status: str
    chunks_created: int
