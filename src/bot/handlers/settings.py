from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from containers import Container
from services.menu_service import SettingsMenuService
from states.menu_states import MenuStates
from utils.const import CallbackName
from utils.user_access import check_user_access


class SettingsHandler:
    def __init__(self, dp: Dispatcher):
        @dp.callback_query(F.data == CallbackName.SETTINGS_CALLBACK)
        async def handle_settings_command(
            callback: CallbackQuery,
            state: FSMContext,
            settings_menu_service: SettingsMenuService = Container.settings_menu_service(),
        ) -> None:
            # TODO вынести возможно в middleware
            user = callback.from_user.username
            if not await check_user_access(user):
                await callback.answer("❌ У вас нет доступа к этому разделу", show_alert=True)
                return

            await state.update_data(previous_state=MenuStates.start)
            await state.set_state(MenuStates.settings)

            settings_keyboard_builder = await settings_menu_service()
            await callback.message.answer(
                "Выберите настройки для редактирования:",
                reply_markup=settings_keyboard_builder.as_markup(resize_keyboard=True),
            )
