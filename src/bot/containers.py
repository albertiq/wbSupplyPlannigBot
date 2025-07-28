from dependency_injector import containers, providers

from api.clients.marketplace_client import MarketplaceAnalyticsClient, MarketplaceSuppliesClient
from db import Database
from repositories.menu_categories import MenuCategoriesRepository
from services.marketplace_service import MarketplaceService
from services.menu_service import MainMenuService, SettingsMenuService, SupplyPlanningMenuService
from services.supply_report_service import SupplyReportService
from settings import cfg


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    db = providers.Singleton(Database)
    menu_categories_repo = providers.Factory(MenuCategoriesRepository, session=db.provided.get_session)
    main_menu_service = providers.Factory(MainMenuService, menu_categories_repo=menu_categories_repo)
    settings_menu_service = providers.Factory(SettingsMenuService, menu_categories_repo=menu_categories_repo)

    marketplace_analytics_api = providers.Singleton(
        MarketplaceAnalyticsClient, base_url=cfg.analytics_api_url, token=cfg.wb_token
    )
    marketplace_supplies_api = providers.Singleton(
        MarketplaceSuppliesClient, base_url=cfg.supplies_api_url, token=cfg.wb_token
    )
    marketplace_service = providers.Factory(
        MarketplaceService, analytics_api_client=marketplace_analytics_api, supplies_api_client=marketplace_supplies_api
    )

    supply_report_service = providers.Factory(SupplyReportService)
    supply_planning_service = providers.Factory(
        SupplyPlanningMenuService, marketplace_service=marketplace_service, supply_report_service=supply_report_service
    )
