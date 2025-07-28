"""insert sections

Revision ID: c205402dabb6
Revises: c4cc0d3fe294
Create Date: 2025-03-08 21:47:14.871333

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "c205402dabb6"
down_revision: Union[str, None] = "c4cc0d3fe294"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sections_table = sa.sql.table("sections", sa.sql.column("name", sa.String))
    menu_categories_table = sa.sql.table(
        "menu_categories",
        sa.sql.column("section_id", sa.Integer),
        sa.sql.column("callback_name", sa.String),
        sa.sql.column("button_text", sa.String),
        sa.sql.column("order_position", sa.Integer),
    )
    op.bulk_insert(sections_table, [{"name": "main_menu"}, {"name": "settings"}])
    op.bulk_insert(
        menu_categories_table,
        [
            {
                "section_id": 1,
                "callback_name": "plan_supplies",
                "button_text": "📋 Запланировать поставки",
                "order_position": 1,
            },
            {"section_id": 1, "callback_name": "get_settings", "button_text": "⚙️ Настройки", "order_position": 2},
            {
                "section_id": 2,
                "callback_name": "set_rules",
                "button_text": "🔄 Задать пороговые значения для заявки",
                "order_position": 2,
            },
            {
                "section_id": 2,
                "callback_name": "set_thresholds",
                "button_text": "🔄 Задать пороговые значения остатков",
                "order_position": 1,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    sections_table = sa.sql.table("sections", sa.sql.column("name", sa.String))
    menu_categories_table = sa.sql.table("menu_categories", sa.sql.column("section_id", sa.Integer))
    op.execute(menu_categories_table.delete().where(menu_categories_table.c.section_id.in_([1, 2])))
    op.execute(sections_table.delete().where(sections_table.c.name.in_(["main_menu", "settings"])))
