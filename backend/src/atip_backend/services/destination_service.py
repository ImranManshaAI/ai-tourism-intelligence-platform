from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from atip_backend.models.destination import Destination


class DestinationService:
    """Service for querying structured destination data."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        *,
        category: str | None = None,
        city: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Destination], int]:
        """Return paginated destinations with optional filters."""

        statement = select(Destination)

        count_statement = select(Destination)

        if category:
            normalized_category = category.strip()

            statement = statement.where(
                Destination.category == normalized_category
            )

            count_statement = count_statement.where(
                Destination.category == normalized_category
            )

        if city:
            normalized_city = city.strip()

            statement = statement.where(
                Destination.city.ilike(
                    f"%{normalized_city}%"
                )
            )

            count_statement = count_statement.where(
                Destination.city.ilike(
                    f"%{normalized_city}%"
                )
            )

        statement = (
            statement
            .order_by(Destination.name)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        destinations = list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

        total = len(
            self.db.execute(count_statement)
            .scalars()
            .all()
        )

        return destinations, total

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
        *,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Destination], int]:
        """Search destinations by name with pagination."""

        normalized_query = query.strip()

        statement = select(Destination).where(
            Destination.name.ilike(
                f"%{normalized_query}%"
            )
        )

        count_statement = select(Destination).where(
            Destination.name.ilike(
                f"%{normalized_query}%"
            )
        )

        statement = (
            statement
            .order_by(Destination.name)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        destinations = list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

        total = len(
            self.db.execute(count_statement)
            .scalars()
            .all()
        )

        return destinations, total

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
