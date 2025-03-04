from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from containers import Container
from services.menu_service import MainMenuService
from states.menu_states import MenuStates
from utils.const import CallbackName


class BackButtonHandler:
    def __init__(self, dp: Dispatcher) -> None:
        @dp.callback_query(F.data == CallbackName.BACK_CALLBACK)
        async def handle_cancel_command(
            callback: CallbackQuery,
            state: FSMContext,
            main_menu_service: MainMenuService = Container.main_menu_service(),
        ):
            data = await state.get_data()
            previous_state = data.get("previous_state")
            if previous_state:
                await state.set_state(previous_state)
                match previous_state:
                    case MenuStates.start:
                        main_keyboard_builder = await main_menu_service()
                        await callback.message.edit_text(
                            "Выберите раздел:", reply_markup=main_keyboard_builder.as_markup(resize_keyboard=True)
                        )
