"""add destination geographic and category fields

Revision ID: 702239d247de
Revises: c6ae3d13bd6d
Create Date: 2026-08-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "702239d247de"
down_revision: Union[str, Sequence[str], None] = "c6ae3d13bd6d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "destinations",
        sa.Column(
            "category",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "destinations",
        sa.Column(
            "city",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "destinations",
        sa.Column(
            "province",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "destinations",
        sa.Column(
            "country",
            sa.String(length=100),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("destinations", "country")
    op.drop_column("destinations", "province")
    op.drop_column("destinations", "city")
    op.drop_column("destinations", "category")
