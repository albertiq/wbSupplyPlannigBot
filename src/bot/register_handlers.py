from aiogram import Dispatcher

from handlers import back, cancel, settings, start, supply_planning, supply_planning_settings, warehouses_settings


def register_all_handlers(dp: Dispatcher) -> None:
    start.StartHandler(dp)
    settings.SettingsHandler(dp)
    supply_planning.SupplyPlanningHandler(dp)
    cancel.CancelHandler(dp)
    back.BackButtonHandler(dp)
    supply_planning_settings.SupplyPlanningSettingsHandler(dp)
    warehouses_settings.WarehousesSettingsHandler(dp)
