from abc import abstractmethod
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from typing import Any

from repositories.menu_categories import MenuCategoriesRepository
from services.base import AsyncBaseService
from utils.const import MainMenuKeyboard, MenuSectionId, SettingsMenuKeyboard


class BaseMenuService(AsyncBaseService):
    def __init__(self, menu_categories_repo: MenuCategoriesRepository):
        self.menu_categories_repo = menu_categories_repo

    @abstractmethod
    async def __call__(self, *args, **kwargs) -> Any:
        pass

    async def get_menu_keyboard_builder(
        self, section_id: int, extra_button: InlineKeyboardButton, button_row_size: int
    ) -> InlineKeyboardBuilder:
        keyboard_builder = InlineKeyboardBuilder()
        menu_categories = await self.menu_categories_repo.get_menu_categories_by_section_id(section_id)
        for category in menu_categories:
            keyboard_builder.button(text=category.button_text, callback_data=category.callback_name)
        keyboard_builder.add(extra_button)
        keyboard_builder.adjust(button_row_size)
        return keyboard_builder


class MainMenuService(BaseMenuService):
    async def __call__(self, section_id: int = MenuSectionId.MAIN_MENU) -> InlineKeyboardBuilder:
        main_keyboard_builder = await self.get_menu_keyboard_builder(
            section_id, MainMenuKeyboard.EXTRA_BUTTON, MainMenuKeyboard.BUTTON_ROW_SIZE
        )
        return main_keyboard_builder


class SettingsMenuService(BaseMenuService):
    async def __call__(self, section_id: int = MenuSectionId.SETTINGS) -> InlineKeyboardBuilder:
        settings_keyboard_builder = await self.get_menu_keyboard_builder(
            section_id, SettingsMenuKeyboard.EXTRA_BUTTON, SettingsMenuKeyboard.BUTTON_ROW_SIZE
        )
        return settings_keyboard_builder
