"""Change attempt user_id to integer

Revision ID: 0d9c2d19d71a
Revises: f4745343a1fe
Create Date: 2026-02-18 12:07:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d9c2d19d71a'
down_revision: Union[str, Sequence[str], None] = 'f4745343a1fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DELETE FROM attempt_answers")
    op.execute("DELETE FROM attempts")

    op.alter_column(
        'attempts',
        'user_id',
        existing_type=sa.Uuid(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using='user_id::text::integer',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM attempt_answers")
    op.execute("DELETE FROM attempts")

    op.alter_column(
        'attempts',
        'user_id',
        existing_type=sa.Integer(),
        type_=sa.Uuid(),
        existing_nullable=False,
        postgresql_using='user_id::text::uuid',
    )
