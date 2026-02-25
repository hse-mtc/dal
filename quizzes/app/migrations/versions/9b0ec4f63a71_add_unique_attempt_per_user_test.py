"""Add unique attempt per user and test

Revision ID: 9b0ec4f63a71
Revises: 0d9c2d19d71a
Create Date: 2026-02-18 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b0ec4f63a71'
down_revision: Union[str, Sequence[str], None] = '0d9c2d19d71a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        DELETE FROM attempt_answers
        WHERE attempt_id IN (
            SELECT a.id
            FROM attempts a
            JOIN (
                SELECT test_id, user_id, MIN(started_at) AS keep_started_at
                FROM attempts
                GROUP BY test_id, user_id
                HAVING COUNT(*) > 1
            ) d ON d.test_id = a.test_id AND d.user_id = a.user_id
            WHERE a.started_at <> d.keep_started_at
        )
        """
    )

    op.execute(
        """
        DELETE FROM attempts a
        USING (
            SELECT test_id, user_id, MIN(started_at) AS keep_started_at
            FROM attempts
            GROUP BY test_id, user_id
            HAVING COUNT(*) > 1
        ) d
        WHERE a.test_id = d.test_id
          AND a.user_id = d.user_id
          AND a.started_at <> d.keep_started_at
        """
    )

    op.create_unique_constraint('uq_attempts_test_user', 'attempts', ['test_id', 'user_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_attempts_test_user', 'attempts', type_='unique')
