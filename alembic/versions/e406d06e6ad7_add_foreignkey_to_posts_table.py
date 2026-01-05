"""add foreignkey to posts table

Revision ID: e406d06e6ad7
Revises: v1.3
Create Date: 2026-01-05 12:45:49.487522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e406d06e6ad7'
down_revision: Union[str, Sequence[str], None] = '3d79f0814523'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("Posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='Posts', referent_table="Users", 
                          local_cols=["user_id"], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name='Posts')
    op.drop_column("Posts", "user_id")
    pass
