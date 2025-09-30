from sqlalchemy.ext.asyncio import async_scoped_session

from models.supply_settings import SupplySettings
from repositories.base import SqlAlchemyRepository


class SupplySettingsRepository(SqlAlchemyRepository):
    def __init__(self, session: async_scoped_session):
        super().__init__(session)

    async def get_supply_settings(self) -> list[SupplySettings]:
        return await self.retrieve_many(
            model=SupplySettings,
        )
