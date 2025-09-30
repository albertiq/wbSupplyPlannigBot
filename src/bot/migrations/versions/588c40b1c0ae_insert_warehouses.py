"""insert warehouses

Revision ID: 588c40b1c0ae
Revises: a2571bdaee8e
Create Date: 2025-09-01 22:25:00.855109

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "588c40b1c0ae"
down_revision: Union[str, None] = "a2571bdaee8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    warehouse_groups_table = sa.sql.table(
        "warehouse_groups",
        sa.sql.column("name"),
    )
    warehouses_table = sa.sql.table("warehouses", sa.sql.column("name"), sa.sql.column("group_id"))

    op.bulk_insert(warehouse_groups_table, [{"name": "Москва"}, {"name": "Казань"}])
    op.bulk_insert(
        warehouses_table,
        [
            {"name": "Краснодар", "group_id": None},
            {"name": "Екатеринбург - Перспективный 12", "group_id": None},
            {"name": "Коледино", "group_id": 1},
            {"name": "Подольск", "group_id": 1},
            {"name": "Электросталь", "group_id": 1},
            {"name": "Тула", "group_id": 1},
            {"name": "Самара (Новосемейкино)", "group_id": 2},
            {"name": "Казань", "group_id": 2},
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    warehouse_groups_table = sa.sql.table(
        "warehouse_groups",
        sa.sql.column("id", sa.Integer),
    )
    warehouses_table = sa.sql.table(
        "warehouses", sa.sql.column("group_id", sa.Integer), sa.sql.column("name", sa.String)
    )
    op.execute(warehouse_groups_table.delete().where(warehouses_table.c.id.in_([1, 2])))
    op.execute(
        warehouses_table.delete().where(
            warehouses_table.c.group_id.in_([1, 2]),
            warehouses_table.c.name.in_(["Краснодар", "Екатеринбург - Перспективный 12"]),
        )
    )
