import json
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from sqlalchemy.exc import DBAPIError

from containers import Container
from keyboards.inline import KeyboardButton
from models import SupplySettings
from services.menu_service import SupplySettingMenuService
from states.menu_states import MenuStates
from utils.const import CallbackName

logger = logging.getLogger(__name__)


class SupplyPlanningSettingsHandler:
    def __init__(self, dp: Dispatcher):
        @dp.callback_query(F.data == CallbackName.SUPPLY_PLANNING_SETTINGS_CALLBACK)
        @dp.callback_query(F.data == CallbackName.REFRESH_SUPPLY_SETTINGS)
        async def show_supply_settings(
            callback: CallbackQuery,
            state: FSMContext,
            supply_settings_menu_service: SupplySettingMenuService = Container.supply_planning_settings_service(),
        ) -> None:
            await state.update_data(previous_state=MenuStates.settings)
            settings = await supply_settings_menu_service.get_settings()
            text = await self._get_settings_text()
            keyboard_builder = await supply_settings_menu_service.get_compact_settings_keyboard(settings)

            if callback.data == CallbackName.REFRESH_SUPPLY_SETTINGS:
                settings = await supply_settings_menu_service.refresh_settings()
                keyboard_builder = await supply_settings_menu_service.get_compact_settings_keyboard(settings)

            if callback.data == CallbackName.REFRESH_SUPPLY_SETTINGS and await self._keyboards_are_identical(
                keyboard_builder.as_markup(), callback.message.reply_markup
            ):
                await callback.answer()
            else:
                await callback.message.edit_text(text, reply_markup=keyboard_builder.as_markup())
            await state.set_state(MenuStates.supply_planning_settings)

        @dp.callback_query(F.data.startswith("quick_edit_"))
        async def edit_supply_setting(
            callback: CallbackQuery,
            state: FSMContext,
            supply_settings_menu_service: SupplySettingMenuService = Container.supply_planning_settings_service(),
        ) -> None:
            await state.update_data(previous_state=MenuStates.supply_planning_settings)
            builder = InlineKeyboardBuilder()
            setting_id = int(callback.data.split("_")[2])
            setting = await supply_settings_menu_service.get_setting(setting_id)

            text = await self._get_edit_prompt_text(setting)
            await state.set_state(MenuStates.edit_supply_planning_setting)

            await callback.message.edit_text(text, reply_markup=builder.add(KeyboardButton.BACK_BUTTON).as_markup())
            await state.update_data(
                editing_setting_id=setting_id,
                original_message_id=callback.message.message_id,
                chat_id=callback.message.chat.id,
            )
            await callback.answer()

        @dp.message(MenuStates.edit_supply_planning_setting)
        async def update_setting(
            message: Message,
            state: FSMContext,
            bot: Bot,
            supply_settings_menu_service: SupplySettingMenuService = Container.supply_planning_settings_service(),
        ):
            builder = InlineKeyboardBuilder()
            try:
                new_value = int(message.text)
            except ValueError:
                await message.answer(
                    "❌ Пожалуйста, введите целое число:",
                    reply_markup=builder.add(KeyboardButton.CANCEL_BUTTON).as_markup(),
                )
                return

            state_data = await state.get_data()
            setting_id = state_data.get("editing_setting_id")
            orig_message_id = state_data.get("original_message_id")
            chat_id = state_data.get("chat_id")

            if not setting_id:
                await message.answer("❌ Ошибка: настройка не выбрана")
                await state.clear()
                return

            setting = await supply_settings_menu_service.get_setting(setting_id)
            if not setting:
                await message.answer("❌ Настройка не найдена")
                await state.clear()
                return

            try:
                await supply_settings_menu_service.update_setting(setting_id, {"value": new_value})

                settings = await supply_settings_menu_service.refresh_settings()
                text = await self._get_settings_text()
                keyboard_builder = await supply_settings_menu_service.get_compact_settings_keyboard(settings)

                try:
                    await message.delete()
                except:
                    pass

                await bot.edit_message_text(
                    chat_id=chat_id, message_id=orig_message_id, text=text, reply_markup=keyboard_builder.as_markup()
                )
                await message.answer(f"✅ <b>{setting.description}</b> обновлено! Новое значение: <b>{new_value}</b>")
                await state.set_state(MenuStates.supply_planning_settings)

            except DBAPIError as e:
                logger.exception(f"Ошибка при обновлении настройки: {e}")
                await message.answer(
                    "❌ Не удалось обновить настройку. Попробуйте еще раз:",
                    reply_markup=builder.add(KeyboardButton.CANCEL_BUTTON).as_markup(),
                )

    @staticmethod
    async def _get_settings_text():
        text = (
            "⚙️ <b>Настройки поставок</b>\n\n" "Нажмите на настройку для редактирования:\n\n" "<b>Текущие значения:</b>"
        )
        return text

    @staticmethod
    async def _get_edit_prompt_text(setting: SupplySettings):
        return (
            f"✏️ <b>{setting.short_name}</b>\n\n"
            f"Текущее значение: <b>{setting.value}</b>\n"
            f"<i>{setting.description}</i>\n\n"
            f"Введите новое значение:"
        )

    @staticmethod
    async def _keyboards_are_identical(
        current_keyboard: InlineKeyboardMarkup, new_keyboard: InlineKeyboardMarkup
    ) -> bool:
        current_kb_str = json.dumps(current_keyboard.model_dump(), sort_keys=True)
        new_kb_str = json.dumps(new_keyboard.model_dump(), sort_keys=True)
        return current_kb_str == new_kb_str
