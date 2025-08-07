from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import LinkPreviewOptions, Message

from containers import Container
from services.menu_service import MainMenuService
from states.menu_states import MenuStates


class StartHandler:
    def __init__(self, dp: Dispatcher) -> None:
        @dp.message(CommandStart())
        async def handle_start_command(
            message: Message, state: FSMContext, main_menu_service: MainMenuService = Container.main_menu_service()
        ) -> None:
            await state.set_state(MenuStates.start)
            await state.update_data(user_message_id=message.message_id)
            main_keyboard_builder = await main_menu_service()
            await message.answer(
                "👋 Привет! Я ваш бот-планировщик поставок! Выберите раздел:",
                reply_markup=main_keyboard_builder.as_markup(resize_keyboard=True),
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
