from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from atip_backend.core.config import get_settings


class DocumentService:
    """Service responsible for validating and storing documents."""

    ALLOWED_CONTENT_TYPES = {
        "application/pdf",
    }

    def __init__(self) -> None:
        self.settings = get_settings()
        self.storage_directory = Path(
            self.settings.document_storage_path
        )

    async def save_uploaded_file(
        self,
        uploaded_file: UploadFile,
    ) -> tuple[str, int]:
        """Validate and securely store an uploaded PDF."""

        if uploaded_file.content_type not in self.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only PDF documents are supported",
            )

        original_suffix = Path(
            uploaded_file.filename or ""
        ).suffix.lower()

        if original_suffix != ".pdf":
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only PDF documents are supported",
            )

        self.storage_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        safe_filename = (
            f"{uuid4()}.pdf"
        )

        storage_path = (
            self.storage_directory / safe_filename
        )

        max_size_bytes = (
            self.settings.max_document_size_mb
            * 1024
            * 1024
        )

        file_size = 0

        try:
            with storage_path.open("wb") as destination:
                while chunk := await uploaded_file.read(
                    1024 * 1024
                ):
                    file_size += len(chunk)

                    if file_size > max_size_bytes:
                        destination.close()
                        storage_path.unlink(
                            missing_ok=True
                        )

                        raise HTTPException(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=(
                                "Document exceeds the maximum "
                                "allowed size"
                            ),
                        )

                    destination.write(chunk)

        except HTTPException:
            raise

        except Exception as exc:
            storage_path.unlink(
                missing_ok=True
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store document",
            ) from exc

        finally:
            await uploaded_file.close()

        return (
            str(storage_path),
            file_size,
        )
