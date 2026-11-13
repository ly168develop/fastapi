"""rename password to password_hash

Revision ID: c66dac464d21
Revises: 04124d57ec40
Create Date: 2026-11-13 11:48:36.079088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c66dac464d21'
down_revision: Union[str, Sequence[str], None] = '04124d57ec40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users",
        "password",
        new_column_name="password_hash"
    )


def downgrade():
    op.alter_column(
        "users",
        "password_hash",
        new_column_name="password"
    )
