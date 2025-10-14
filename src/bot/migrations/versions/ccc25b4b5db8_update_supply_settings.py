"""update supply_settings

Revision ID: ccc25b4b5db8
Revises: b216be76f6f5
Create Date: 2025-10-14 13:20:37.836786

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "ccc25b4b5db8"
down_revision: Union[str, None] = "b216be76f6f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    data_to_update = [
        {"name": "max_to_client_low", "short_name": "Макс. малый заказ"},
        {"name": "max_to_client_medium", "short_name": "Макс. средний заказ"},
        {"name": "warehouse_remains_threshold", "short_name": "Мин. остаток"},
        {"name": "total_threshold", "short_name": "Общий порог"},
        {"name": "quantity_small", "short_name": "Малый заказ"},
        {"name": "quantity_medium", "short_name": "Средний заказ"},
        {"name": "quantity_large", "short_name": "Большой заказ"},
        {"name": "min_to_client_threshold", "short_name": "Мин. для заявки"},
    ]
    conn.execute(
        sa.text("""
          UPDATE supply_settings
          SET short_name = :short_name
          WHERE name = :name
          """),
        data_to_update,
    )


def downgrade() -> None:
    """Downgrade schema."""

    conn = op.get_bind()
    data_to_update = [
        {"name": "max_to_client_low", "short_name": None},
        {"name": "max_to_client_medium", "short_name": None},
        {"name": "warehouse_remains_threshold", "short_name": None},
        {"name": "total_threshold", "short_name": None},
        {"name": "quantity_small", "short_name": None},
        {"name": "quantity_medium", "short_name": None},
        {"name": "quantity_large", "short_name": None},
        {"name": "min_to_client_threshold", "short_name": None},
    ]
    conn.execute(
        sa.text("""
              UPDATE supply_settings
              SET short_name = :short_name
              WHERE name = :name
              """),
        data_to_update,
    )
