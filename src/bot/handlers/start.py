from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


class StartHandler:
    def __init__(self, dp: Dispatcher) -> None:
        @dp.message(CommandStart())
        async def start_command(message: Message):
            await message.answer("Привет! Я ваш бот-планировщик поставок! Выберите раздел.")
