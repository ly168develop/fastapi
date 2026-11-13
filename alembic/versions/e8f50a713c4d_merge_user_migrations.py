"""Merge the duplicate user migration branches.

Revision ID: e8f50a713c4d
Revises: 33a9fe7b8b3a, 4119d3b2063c
"""

from typing import Sequence, Union

revision: str = 'e8f50a713c4d'
down_revision: Union[str, Sequence[str], None] = ('33a9fe7b8b3a', '4119d3b2063c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
