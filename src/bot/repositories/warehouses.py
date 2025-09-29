from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.orm import joinedload

from models.warehouses import WarehouseGroups, Warehouses
from repositories.base import SqlAlchemyRepository


class WarehousesRepository(SqlAlchemyRepository):
    def __init__(self, session: async_scoped_session):
        super().__init__(session)

    async def get_warehouses(self) -> list[Warehouses]:
        return await self.retrieve_many(
            model=Warehouses,
            join_models=[(WarehouseGroups, Warehouses.group_id == WarehouseGroups.id)],
            join_type="left",
            options=[joinedload(Warehouses.group)],
        )
