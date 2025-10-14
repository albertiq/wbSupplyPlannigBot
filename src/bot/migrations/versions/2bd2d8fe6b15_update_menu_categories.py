"""update menu_categories

Revision ID: 2bd2d8fe6b15
Revises: dda0e878a30a
Create Date: 2025-09-30 23:19:22.753242

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "2bd2d8fe6b15"
down_revision: Union[str, None] = "dda0e878a30a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    menu_categories_table = sa.sql.table(
        "menu_categories",
        sa.sql.column("section_id", sa.Integer),
        sa.sql.column("callback_name", sa.String),
        sa.sql.column("button_text", sa.String),
    )
    op.execute(
        menu_categories_table.update()
        .where(menu_categories_table.c.section_id == 2, menu_categories_table.c.callback_name == "set_thresholds")
        .values(
            {"button_text": "🔧 Настройки пороговых значений поставок", "callback_name": "supply_thresholds_settings"}
        )
    )
    op.execute(
        menu_categories_table.update()
        .where(menu_categories_table.c.section_id == 2, menu_categories_table.c.callback_name == "set_rules")
        .values({"button_text": "🔧 Настройки складов", "callback_name": "warehouses_settings"})
    )


def downgrade() -> None:
    """Downgrade schema."""
    menu_categories_table = sa.sql.table(
        "menu_categories",
        sa.sql.column("section_id", sa.Integer),
        sa.sql.column("callback_name", sa.String),
        sa.sql.column("button_text", sa.String),
    )
    op.execute(
        menu_categories_table.update()
        .where(
            menu_categories_table.c.section_id == 2,
            menu_categories_table.c.callback_name == "supply_thresholds_settings",
        )
        .values({"button_text": "🔄 Задать пороговые значения остатков", "callback_name": "set_thresholds"})
    )
    op.execute(
        menu_categories_table.update()
        .where(menu_categories_table.c.section_id == 2, menu_categories_table.c.callback_name == "warehouses_settings")
        .values({"button_text": "🔄 Задать пороговые значения для заявки", "callback_name": "set_rules"})
    )
