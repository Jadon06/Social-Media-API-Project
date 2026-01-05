"""add last few columns to post table

Revision ID: 609a924654ab
Revises: e406d06e6ad7
Create Date: 2026-01-05 12:58:57.602287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '609a924654ab'
down_revision: Union[str, Sequence[str], None] = 'e406d06e6ad7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Posts', sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('Posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, sever_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("Posts", "published")
    op.drop_column("Posts", "created_at")
    pass
