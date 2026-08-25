"""add hnsw embedding index

Revision ID: add_hnsw_embedding_index
Revises: 9a37dd87708a
Create Date: 2026-08-17
"""

from typing import Sequence, Union

from alembic import op


revision: str = "add_hnsw_embedding_index"
down_revision: Union[str, Sequence[str], None] = "9a37dd87708a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE INDEX ix_document_chunks_embedding_hnsw
        ON document_chunks
        USING hnsw (embedding vector_cosine_ops)
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX IF EXISTS ix_document_chunks_embedding_hnsw
        """
    )
