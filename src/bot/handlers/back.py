from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from containers import Container
from services.menu_service import MainMenuService, SettingsMenuService, SupplyPlanningMenuService
from states.menu_states import MenuStates
from utils.const import CallbackName


class BackButtonHandler:
    def __init__(self, dp: Dispatcher) -> None:
        @dp.callback_query(F.data == CallbackName.BACK_CALLBACK)
        async def handle_back_command(
            callback: CallbackQuery,
            state: FSMContext,
            main_menu_service: MainMenuService = Container.main_menu_service(),
            settings_menu_service: SettingsMenuService = Container.settings_menu_service(),
            supply_settings_menu_service: SupplyPlanningMenuService = Container.supply_planning_settings_service(),
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
                    case MenuStates.settings:
                        await state.update_data(previous_state=MenuStates.start)

                        settings_keyboard_builder = await settings_menu_service()
                        await callback.message.edit_text(
                            "Выберите настройки для редактирования:",
                            reply_markup=settings_keyboard_builder.as_markup(resize_keyboard=True),
                        )
                    case MenuStates.supply_planning_settings:
                        await state.update_data(previous_state=MenuStates.settings)

                        supply_settings_builder = await supply_settings_menu_service()
                        await callback.message.edit_text(
                            "Нажмите на настройку для редактирования:",
                            reply_markup=supply_settings_builder.as_markup(resize_keyboard=True),
                        )
