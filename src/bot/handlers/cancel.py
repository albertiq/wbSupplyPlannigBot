from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils.const import CallbackName


class CancelHandler:
    def __init__(self, dp: Dispatcher) -> None:
        @dp.callback_query(F.data == CallbackName.CANCEL_CALLBACK)
        async def handle_cancel_command(callback: CallbackQuery, state: FSMContext):
            await state.clear()
            await callback.message.delete()
