from aiogram import Dispatcher

from handlers import start


def register_all_handlers(dp: Dispatcher) -> None:
    start.StartHandler(dp)
