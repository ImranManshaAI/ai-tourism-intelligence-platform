from uuid import UUID

from sqlalchemy.orm import Session

from atip_backend.models.document import Document
from atip_backend.models.document_chunk import DocumentChunk
from atip_backend.services.document_chunker import DocumentChunker
from atip_backend.services.document_extractor import DocumentExtractor


class DocumentProcessingService:
    """Extract, chunk, and persist document content."""

    def __init__(
        self,
        extractor: DocumentExtractor | None = None,
        chunker: DocumentChunker | None = None,
    ) -> None:
        self.extractor = extractor or DocumentExtractor()
        self.chunker = chunker or DocumentChunker()

    def process_document(
        self,
        db: Session,
        document_id: UUID,
    ) -> int:
        """Process an uploaded document and store its text chunks."""

        document = db.get(
            Document,
            document_id,
        )

        if document is None:
            raise ValueError(
                "Document not found"
            )

        pages = self.extractor.extract_pdf(
            document.storage_path
        )

        chunks = self.chunker.chunk_pages(
            pages
        )

        db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document.id
        ).delete()

        for chunk in chunks:
            db.add(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=chunk["chunk_index"],
                    content=chunk["content"],
                    page_number=chunk["page_number"],
                )
            )

        document.status = "processed"

        db.flush()

        return len(chunks)
