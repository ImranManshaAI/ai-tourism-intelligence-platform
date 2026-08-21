from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from atip_backend.models.destination import Destination


class DestinationService:
    """Service for querying structured destination data."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Destination]:
        """Return all destinations ordered by name."""

        statement = (
            select(Destination)
            .order_by(Destination.name)
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def get_by_id(
        self,
        destination_id: UUID,
    ) -> Destination | None:
        """Return a destination by its ID."""

        return self.db.get(
            Destination,
            destination_id,
        )

    def search(
        self,
        query: str,
    ) -> list[Destination]:
        """Search destinations by name."""

        statement = (
            select(Destination)
            .where(
                Destination.name.ilike(
                    f"%{query.strip()}%"
                )
            )
            .order_by(Destination.name)
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def get_by_category(
        self,
        category: str,
    ) -> list[Destination]:
        """Return destinations matching a category."""

        statement = (
            select(Destination)
            .where(
                Destination.category == category.strip()
            )
            .order_by(Destination.name)
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def get_by_city(
        self,
        city: str,
    ) -> list[Destination]:
        """Return destinations matching a city."""

        statement = (
            select(Destination)
            .where(
                Destination.city.ilike(
                    f"%{city.strip()}%"
                )
            )
            .order_by(Destination.name)
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )