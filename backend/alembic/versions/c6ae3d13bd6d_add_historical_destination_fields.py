"""add historical destination fields

Revision ID: c6ae3d13bd6d
Revises: add_hnsw_embedding_index
Create Date: 2026-08-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c6ae3d13bd6d"
down_revision: Union[str, Sequence[str], None] = "add_hnsw_embedding_index"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "destinations",
        sa.Column("location_text", sa.Text(), nullable=True),
    )

    op.add_column(
        "destinations",
        sa.Column("built_by", sa.Text(), nullable=True),
    )

    op.add_column(
        "destinations",
        sa.Column("year_built", sa.String(length=500), nullable=True),
    )

    op.add_column(
        "destinations",
        sa.Column("source_verification", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("destinations", "source_verification")
    op.drop_column("destinations", "year_built")
    op.drop_column("destinations", "built_by")
    op.drop_column("destinations", "location_text")
