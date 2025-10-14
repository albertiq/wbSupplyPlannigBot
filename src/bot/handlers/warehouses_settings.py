from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery

from utils.const import CallbackName


class WarehousesSettingsHandler:
    def __init__(self, dp: Dispatcher):
        @dp.callback_query(F.data == CallbackName.WAREHOUSES_SETTINGS)
        async def handle_warehouses_settings_command(
            callback: CallbackQuery,
        ) -> None:
            await callback.answer(
                text="⚙️ Раздел настроек складов находится в разработке. Скоро будет доступен!", show_alert=True
            )
