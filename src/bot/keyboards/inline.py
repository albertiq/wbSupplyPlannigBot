from aiogram.utils.keyboard import InlineKeyboardButton

from settings import cfg


class KeyboardButton:
    CANCEL_BUTTON = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    BACK_BUTTON = InlineKeyboardButton(text="⬅️ Назад", callback_data="back")
    SUPPORT_BUTTON = InlineKeyboardButton(
        text="✉️ Написать в поддержку",
        url=f"tg://resolve?domain={cfg.support_username}",
    )
