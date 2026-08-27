from pathlib import Path
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
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
    DocumentResponse,
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
