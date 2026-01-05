"""add content column

Revision ID: 9be06fdb3ead
Revises: 709be195da3e
Create Date: 2026-01-05 12:24:08.078069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9be06fdb3ead'
down_revision: Union[str, Sequence[str], None] = '709be195da3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("Posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("Posts", "content")
    pass
