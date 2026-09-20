"""changement autincrement pk de emprunt

Revision ID: 53d2d13767d4
Revises: 06d4ff5f0805
Create Date: 2026-09-20 16:12:04.519903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53d2d13767d4'
down_revision: Union[str, Sequence[str], None] = '06d4ff5f0805'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
