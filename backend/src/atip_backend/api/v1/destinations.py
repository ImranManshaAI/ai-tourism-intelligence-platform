from typing import Generator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from atip_backend.db.session import SessionLocal
from atip_backend.schemas.destination import (
    DestinationResponse,
    PaginatedDestinationResponse,
)
from atip_backend.services.destination_service import DestinationService


router = APIRouter(
    prefix="/destinations",
    tags=["Destinations"],
)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for each request."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "",
    response_model=PaginatedDestinationResponse,
)
def get_destinations(
    category: str | None = Query(
        default=None,
        min_length=1,
    ),
    city: str | None = Query(
        default=None,
        min_length=1,
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
) -> PaginatedDestinationResponse:
    """Get paginated destinations with optional filters."""

    service = DestinationService(db)

    destinations, total = service.get_all(
        category=category,
        city=city,
        page=page,
        page_size=page_size,
    )

    items = [
        DestinationResponse.model_validate(
            destination
        )
        for destination in destinations
    ]

    return PaginatedDestinationResponse.create(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/search",
    response_model=PaginatedDestinationResponse,
)
def search_destinations(
    q: str = Query(
        ...,
        min_length=1,
        description="Search destination names",
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
) -> PaginatedDestinationResponse:
    """Search destinations by name with pagination."""

    service = DestinationService(db)

    destinations, total = service.search(
        q,
        page=page,
        page_size=page_size,
    )

    items = [
        DestinationResponse.model_validate(
            destination
        )
        for destination in destinations
    ]

    return PaginatedDestinationResponse.create(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{destination_id}",
    response_model=DestinationResponse,
)
def get_destination(
    destination_id: UUID,
    db: Session = Depends(get_db),
) -> DestinationResponse:
    """Get a single destination by ID."""

    service = DestinationService(db)

    destination = service.get_by_id(destination_id)

    if destination is None:
        raise HTTPException(
            status_code=404,
            detail="Destination not found",
        )

    return DestinationResponse.model_validate(
        destination
    )
