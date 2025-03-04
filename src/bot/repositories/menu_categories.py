from sqlalchemy.ext.asyncio import async_scoped_session

from models.menu import MenuCategories
from repositories.base import SqlAlchemyRepository


class MenuCategoriesRepository(SqlAlchemyRepository):
    def __init__(self, session: async_scoped_session):
        super().__init__(session)

    async def get_menu_categories_by_section_id(self, section_id: int) -> list[MenuCategories]:
        return await self.retrieve_many(
            model=MenuCategories,
            where_clause=[MenuCategories.section_id == section_id],
            order_by=[MenuCategories.section_id, MenuCategories.order_position],
        )
