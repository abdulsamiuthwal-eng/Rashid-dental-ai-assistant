"""Create appointments table

Revision ID: 0001
Revises:
Create Date: 2026-07-15

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("patient_name", sa.String(length=200), nullable=False, index=True),
        sa.Column("contact_number", sa.String(length=50), nullable=False),
        sa.Column("preferred_date", sa.Date(), nullable=False),
        sa.Column("preferred_time", sa.String(length=20), nullable=False),
        sa.Column("requested_service", sa.String(length=200), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("appointments")
