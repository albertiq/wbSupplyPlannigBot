from aiogram import Dispatcher

from handlers import back, cancel, settings, start


def register_all_handlers(dp: Dispatcher) -> None:
    start.StartHandler(dp)
    settings.SettingsHandler(dp)
    cancel.CancelHandler(dp)
    back.BackButtonHandler(dp)
