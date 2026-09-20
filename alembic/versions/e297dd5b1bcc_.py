"""empty message

Revision ID: e297dd5b1bcc
Revises: 53d2d13767d4
Create Date: 2026-09-20 16:20:57.349939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e297dd5b1bcc'
down_revision: Union[str, Sequence[str], None] = '53d2d13767d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("emprunts")
    op.create_table(
        "emprunts",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("book_id", sa.Integer, sa.ForeignKey("livres.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("emprunts")