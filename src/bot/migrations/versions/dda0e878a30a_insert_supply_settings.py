"""insert supply_settings

Revision ID: dda0e878a30a
Revises: 80a066b0fe30
Create Date: 2025-09-30 11:39:17.878398

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "dda0e878a30a"
down_revision: Union[str, None] = "80a066b0fe30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    supply_settings_table = sa.sql.table(
        "supply_settings", sa.sql.column("name"), sa.sql.column("value"), sa.sql.column("description")
    )
    op.bulk_insert(
        supply_settings_table,
        [
            {
                "name": "min_to_client_threshold",
                "value": 3,
                "description": "Минимальное количество товаров в пути для формирования заявки",
            },
            {
                "name": "max_to_client_low",
                "value": 10,
                "description": "Верхняя граница для малого количества товаров в пути",
            },
            {
                "name": "max_to_client_medium",
                "value": 20,
                "description": "Верхняя граница для среднего количества товаров в пути",
            },
            {"name": "warehouse_remains_threshold", "value": 5, "description": "Порог остатков на складе"},
            {"name": "total_threshold", "value": 50, "description": "Порог общего количества товаров"},
            {
                "name": "quantity_small",
                "value": 5,
                "description": "Количество для заказа при малом количестве товаров в пути",
            },
            {
                "name": "quantity_medium",
                "value": 10,
                "description": "Количество для заказа при среднем количестве товаров в пути",
            },
            {
                "name": "quantity_large",
                "value": 20,
                "description": "Количество для заказа при большом количестве товаров в пути",
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    supply_settings_table = sa.sql.table("supply_settings", sa.sql.column("name", sa.String()))
    op.execute(
        supply_settings_table.delete().where(
            supply_settings_table.c.name.in_(
                [
                    "min_to_client_threshold",
                    "max_to_client_low",
                    "max_to_client_medium",
                    "warehouse_remains_threshold",
                    "total_threshold",
                    "quantity_small",
                    "quantity_medium",
                    "quantity_large",
                ]
            )
        )
    )
