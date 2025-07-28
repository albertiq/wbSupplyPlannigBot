from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from containers import Container
from services.menu_service import SettingsMenuService
from states.menu_states import MenuStates
from utils.const import CallbackName


class SettingsHandler:
    def __init__(self, dp: Dispatcher):
        @dp.callback_query(F.data == CallbackName.SETTINGS_CALLBACK)
        async def handle_settings_command(
            callback: CallbackQuery,
            state: FSMContext,
            settings_menu_service: SettingsMenuService = Container.settings_menu_service(),
        ) -> None:
            await state.update_data(previous_state=MenuStates.start)
            await state.set_state(MenuStates.settings)

            await callback.answer(
                text="⚙️ Раздел настроек находится в разработке. Скоро будет доступен!", show_alert=True
            )
            # settings_keyboard_builder = await settings_menu_service()
            # await callback.message.answer(
            #     "Выберите настройки для редактирования:",
            #     reply_markup=settings_keyboard_builder.as_markup(resize_keyboard=True),
            # )
            # TODO Добавить кнопки по изменению пороговых значений + добавлению/удалению складов
