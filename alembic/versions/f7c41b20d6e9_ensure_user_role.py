"""Ensure users.role exists on databases stamped by the empty role revision.

Revision ID: f7c41b20d6e9
Revises: e8f50a713c4d
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'f7c41b20d6e9'
down_revision: Union[str, Sequence[str], None] = 'e8f50a713c4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    columns = {column['name'] for column in sa.inspect(op.get_bind()).get_columns('users')}
    if 'role' not in columns:
        op.add_column('users', sa.Column('role', sa.String(length=20), nullable=False, server_default='user'))


def downgrade() -> None:
    # The preceding role revision also creates this column on fresh databases.
    pass
