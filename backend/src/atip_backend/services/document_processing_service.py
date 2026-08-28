from uuid import UUID

from sqlalchemy.orm import Session

from atip_backend.models.document import Document
from atip_backend.models.document_chunk import DocumentChunk
from atip_backend.services.document_chunker import DocumentChunker
from atip_backend.services.document_extractor import DocumentExtractor
from atip_backend.services.embedding_service import EmbeddingService


class DocumentProcessingService:
    """Extract, chunk, embed, and persist document content."""

    def __init__(
        self,
        extractor: DocumentExtractor | None = None,
        chunker: DocumentChunker | None = None,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.extractor = extractor or DocumentExtractor()
        self.chunker = chunker or DocumentChunker()
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

    def process_document(
        self,
        db: Session,
        document_id: UUID,
    ) -> int:
        """Process an uploaded document and store embedded text chunks."""

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

        if chunks:
            embeddings = self.embedding_service.embed_texts(
                [
                    chunk["content"]
                    for chunk in chunks
                ]
            )

            for chunk, embedding in zip(
                chunks,
                embeddings,
                strict=True,
            ):
                db.add(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=chunk["chunk_index"],
                        content=chunk["content"],
                        page_number=chunk["page_number"],
                        embedding=embedding,
                    )
                )

        document.status = "processed"

        db.flush()

        return len(chunks)
