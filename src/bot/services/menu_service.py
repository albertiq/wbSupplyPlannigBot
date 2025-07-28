from abc import abstractmethod
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from typing import Any

from repositories.menu_categories import MenuCategoriesRepository
from services.base import AsyncBaseService
from services.marketplace_service import MarketplaceService
from services.supply_report_service import SupplyReportService
from utils.const import MainMenuKeyboard, MenuSectionId, SettingsMenuKeyboard


class BaseMenuService(AsyncBaseService):
    @abstractmethod
    async def __call__(self, *args, **kwargs) -> Any:
        pass

    @staticmethod
    async def get_menu_keyboard_builder(
        menu_categories_repo: MenuCategoriesRepository,
        section_id: int,
        extra_button: InlineKeyboardButton,
        button_row_size: int,
    ) -> InlineKeyboardBuilder:
        keyboard_builder = InlineKeyboardBuilder()
        menu_categories = await menu_categories_repo.get_menu_categories_by_section_id(section_id)
        for category in menu_categories:
            keyboard_builder.button(text=category.button_text, callback_data=category.callback_name)
        keyboard_builder.add(extra_button)
        keyboard_builder.adjust(button_row_size)
        return keyboard_builder


class MainMenuService(BaseMenuService):
    def __init__(self, menu_categories_repo: MenuCategoriesRepository):
        self.menu_categories_repo = menu_categories_repo

    async def __call__(self, section_id: int = MenuSectionId.MAIN_MENU) -> InlineKeyboardBuilder:
        main_keyboard_builder = await self.get_menu_keyboard_builder(
            self.menu_categories_repo, section_id, MainMenuKeyboard.EXTRA_BUTTON, MainMenuKeyboard.BUTTON_ROW_SIZE
        )
        return main_keyboard_builder


class SettingsMenuService(BaseMenuService):
    def __init__(self, menu_categories_repo: MenuCategoriesRepository):
        self.menu_categories_repo = menu_categories_repo

    async def __call__(self, section_id: int = MenuSectionId.SETTINGS) -> InlineKeyboardBuilder:
        settings_keyboard_builder = await self.get_menu_keyboard_builder(
            self.menu_categories_repo,
            section_id,
            SettingsMenuKeyboard.EXTRA_BUTTON,
            SettingsMenuKeyboard.BUTTON_ROW_SIZE,
        )
        return settings_keyboard_builder


class SupplyPlanningMenuService(BaseMenuService):
    def __init__(self, marketplace_service: MarketplaceService, supply_report_service: SupplyReportService):
        self.marketplace_service = marketplace_service
        self.supply_report_service = supply_report_service

    async def __call__(self, section_id: int = MenuSectionId.SUPPLY_PLANNING) -> Any:
        planned_supplies = await self.marketplace_service()
        return await self.supply_report_service(planned_supplies)
