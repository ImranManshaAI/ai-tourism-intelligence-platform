from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from atip_backend.db.base import Base


class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Geographic and classification fields
    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    province: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Historical and source fields
    location_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    built_by: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    year_built: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    source_verification: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Coordinates
    latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    # Tourism information
    ticket_price: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    opening_hours: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    facilities: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    travel_tips: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    images: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
