"""create warehouses

Revision ID: a2571bdaee8e
Revises: c205402dabb6
Create Date: 2025-09-01 22:16:23.939978

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "a2571bdaee8e"
down_revision: Union[str, None] = "c205402dabb6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "warehouse_groups",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "warehouses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.ForeignKeyConstraint(["group_id"], ["warehouse_groups.id"], ondelete="set null"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("warehouses")
    op.drop_table("warehouse_groups")
