from dependency_injector import containers, providers

from db import Database
from repositories.menu_categories import MenuCategoriesRepository
from services.menu_service import MainMenuService, SettingsMenuService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    db = providers.Singleton(Database)
    menu_categories_repo = providers.Factory(MenuCategoriesRepository, session=db.provided.get_session)
    main_menu_service = providers.Factory(MainMenuService, menu_categories_repo=menu_categories_repo)
    settings_menu_service = providers.Factory(SettingsMenuService, menu_categories_repo=menu_categories_repo)
