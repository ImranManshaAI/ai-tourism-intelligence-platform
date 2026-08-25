from typing import Generator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from atip_backend.db.session import SessionLocal
from atip_backend.schemas.destination import DestinationResponse
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
    response_model=list[DestinationResponse],
)
def get_destinations(
    category: str | None = None,
    city: str | None = None,
    db: Session = Depends(get_db),
):
    """Get all destinations with optional filters."""

    service = DestinationService(db)

    if category:
        return service.get_by_category(category)

    if city:
        return service.get_by_city(city)

    return service.get_all()


@router.get(
    "/search",
    response_model=list[DestinationResponse],
)
def search_destinations(
    q: str = Query(
        ...,
        min_length=1,
        description="Search destination names",
    ),
    db: Session = Depends(get_db),
):
    """Search destinations by name."""

    service = DestinationService(db)

    return service.search(q)


@router.get(
    "/{destination_id}",
    response_model=DestinationResponse,
)
def get_destination(
    destination_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single destination by ID."""

    service = DestinationService(db)

    destination = service.get_by_id(destination_id)

    if destination is None:
        raise HTTPException(
            status_code=404,
            detail="Destination not found",
        )

    return destination
