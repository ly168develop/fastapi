"""add user role

Revision ID: 33a9fe7b8b3a
Revises: b11b3b1fbf93
Create Date: 2026-11-13 12:43:30.124481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33a9fe7b8b3a'
down_revision: Union[str, Sequence[str], None] = 'b11b3b1fbf93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('role', sa.String(length=20), server_default='user', nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
