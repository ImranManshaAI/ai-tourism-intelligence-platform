from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DestinationResponse(BaseModel):
    """Destination data returned by the API."""

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    name: str
    description: str

    category: str | None = None

    city: str | None = None
    province: str | None = None
    country: str | None = None

    location_text: str | None = None
    built_by: str | None = None
    year_built: str | None = None
    source_verification: str | None = None

    latitude: Decimal | None = None
    longitude: Decimal | None = None

    ticket_price: Decimal | None = None

    opening_hours: dict | None = None
    facilities: list | None = None
    travel_tips: list | None = None
    images: list | None = None

    created_at: datetime
    updated_at: datetime
