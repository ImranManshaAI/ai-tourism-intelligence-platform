from pathlib import Path
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from atip_backend.api.deps import (
    get_current_user,
    get_db,
)
from atip_backend.models.document import Document
from atip_backend.models.user import User
from atip_backend.schemas.document import (
    DocumentProcessResponse,
    DocumentResponse,
)
from atip_backend.services.document_processing_service import (
    DocumentProcessingService,
)
from atip_backend.services.document_service import (
    DocumentService,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Document:
    """Upload and store a PDF document."""

    service = DocumentService()

    try:
        storage_path, file_size = await service.save_uploaded_file(
            file
        )
        storage_path = Path(storage_path)

        document = Document(
            filename=storage_path.name,
            original_filename=file.filename,
            content_type=file.content_type,
            file_size=file_size,
            storage_path=str(storage_path),
            status="uploaded",
            created_by=current_user.id,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    except Exception:
        db.rollback()
        raise


@router.post(
    "/{document_id}/process",
    response_model=DocumentProcessResponse,
)
def process_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentProcessResponse:
    """Extract and chunk an uploaded document."""

    document = db.get(
        Document,
        document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    service = DocumentProcessingService()

    try:
        chunks_created = service.process_document(
            db=db,
            document_id=document_id,
        )

        db.commit()

        return DocumentProcessResponse(
            document_id=document.id,
            status=document.status,
            chunks_created=chunks_created,
        )

    except Exception:
        db.rollback()
        raise
