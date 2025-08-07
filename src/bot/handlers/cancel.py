from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils.const import CallbackName


class CancelHandler:
    def __init__(self, dp: Dispatcher) -> None:
        @dp.callback_query(F.data == CallbackName.CANCEL_CALLBACK)
        async def handle_cancel_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
            state_data = await state.get_data()
            if "user_message_id" in state_data:
                await bot.delete_message(chat_id=callback.message.chat.id, message_id=state_data["user_message_id"])
            await callback.message.delete()
            await state.clear()
