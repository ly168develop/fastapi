"""rename the hash_password

Revision ID: 4119d3b2063c
Revises: 04124d57ec40
Create Date: 2026-11-13 11:45:03.197342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4119d3b2063c'
down_revision: Union[str, Sequence[str], None] = '04124d57ec40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Superseded by c66dac464d21 and b11b3b1fbf93 on the other branch.
    # Keep this revision so databases stamped with it remain recognizable.
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
