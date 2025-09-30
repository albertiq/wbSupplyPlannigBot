from typing import Any

from repositories.supply_settings import SupplySettingsRepository
from services.base import AsyncBaseService


class SupplySettingService(AsyncBaseService):
    def __init__(self, supply_settings_repo: SupplySettingsRepository):
        self.supply_settings_repo = supply_settings_repo
        self._cache = None

    async def __call__(self, *args, **kwargs) -> Any:
        return await self.get_settings()

    async def get_settings(self) -> dict[str, int]:
        if self._cache is None:
            settings = await self.supply_settings_repo.get_supply_settings()
            self._cache = {setting.name: setting.value for setting in settings}
        return self._cache

    async def refresh_settings(self):
        self._cache = None
        await self.get_settings()
