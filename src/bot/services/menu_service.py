from abc import abstractmethod
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from typing import Any

from models import SupplySettings
from repositories.menu_categories import MenuCategoriesRepository
from repositories.supply_settings import SupplySettingsRepository
from services.base import AsyncBaseService
from services.marketplace_service import MarketplaceService
from services.supply_report_service import SupplyReportService
from utils.const import MainMenuKeyboard, MenuSectionId, SettingsMenuKeyboard, SupportMenuKeyboard


class BaseMenuService(AsyncBaseService):
    @abstractmethod
    async def __call__(self, *args, **kwargs) -> Any:
        pass

    # TODO подумать как сделать метод универсальным для всех меню
    @staticmethod
    async def get_menu_keyboard_builder(
        menu_categories_repo: MenuCategoriesRepository,
        section_id: int,
        extra_buttons: list[InlineKeyboardButton],
        button_row_size: int,
    ) -> InlineKeyboardBuilder:
        keyboard_builder = InlineKeyboardBuilder()
        menu_categories = await menu_categories_repo.get_menu_categories_by_section_id(section_id)
        for category in menu_categories:
            keyboard_builder.button(text=category.button_text, callback_data=category.callback_name)
        for extra_button in extra_buttons:
            keyboard_builder.add(extra_button)
        keyboard_builder.adjust(button_row_size)
        return keyboard_builder


class MainMenuService(BaseMenuService):
    def __init__(self, menu_categories_repo: MenuCategoriesRepository):
        self.menu_categories_repo = menu_categories_repo

    async def __call__(self, section_id: int = MenuSectionId.MAIN_MENU) -> InlineKeyboardBuilder:
        main_keyboard_builder = await self.get_menu_keyboard_builder(
            self.menu_categories_repo,
            section_id,
            [SupportMenuKeyboard.SUPPORT_BUTTON, MainMenuKeyboard.EXTRA_BUTTON],
            MainMenuKeyboard.BUTTON_ROW_SIZE,
        )
        return main_keyboard_builder


class SettingsMenuService(BaseMenuService):
    def __init__(self, menu_categories_repo: MenuCategoriesRepository):
        self.menu_categories_repo = menu_categories_repo

    async def __call__(self, section_id: int = MenuSectionId.SETTINGS) -> InlineKeyboardBuilder:
        settings_keyboard_builder = await self.get_menu_keyboard_builder(
            self.menu_categories_repo,
            section_id,
            [SettingsMenuKeyboard.EXTRA_BUTTON],
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


class SupplySettingMenuService(BaseMenuService):
    def __init__(self, supply_settings_repo: SupplySettingsRepository):
        self.supply_settings_repo = supply_settings_repo
        self._cache = None

    async def __call__(self, *args, **kwargs) -> Any:
        return await self.get_compact_settings_keyboard(await self.get_settings())

    async def get_settings(self) -> list[SupplySettings]:
        if self._cache is None:
            settings = await self.supply_settings_repo.get_supply_settings()
            self._cache = settings
        return self._cache

    async def get_setting(self, setting_id: int) -> SupplySettings:
        return await self.supply_settings_repo.get_supply_setting_by_id(setting_id)

    async def refresh_settings(self) -> list[SupplySettings]:
        self._cache = None
        return await self.get_settings()

    async def update_setting(self, setting_id: int, new_values: dict) -> None:
        await self.supply_settings_repo.update_setting(setting_id, new_values)

    # TODO методы с клавиатурами убрать после того, как зауниверсалим BaseMenuService.get_menu_keyboard_builder()
    @staticmethod
    async def get_compact_settings_keyboard(settings: list[SupplySettings]) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()

        for setting in settings:
            builder.button(text=f"⚙️ {setting.short_name}: {setting.value}", callback_data=f"quick_edit_{setting.id}")

        builder.add(SettingsMenuKeyboard.REFRESH_BUTTON)
        builder.add(SettingsMenuKeyboard.EXTRA_BUTTON)
        builder.adjust(SettingsMenuKeyboard.BUTTON_ROW_SIZE)
        return builder
