from aiogram.utils.keyboard import InlineKeyboardButton


class KeyboardButton:
    CANCEL_BUTTON = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    BACK_BUTTON = InlineKeyboardButton(text="⬅️ Назад", callback_data="back")
