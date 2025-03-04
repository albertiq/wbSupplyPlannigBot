from keyboards.inline import KeyboardButton


class CallbackName:
    SETTINGS_CALLBACK = "get_settings"
    BACK_CALLBACK = "back"
    CANCEL_CALLBACK = "cancel"


class MenuSectionId:
    MAIN_MENU = 1
    SETTINGS = 2
    WAREHOUSES = 3


class MainMenuKeyboard:
    EXTRA_BUTTON = KeyboardButton.CANCEL_BUTTON
    BUTTON_ROW_SIZE = 2


class SettingsMenuKeyboard:
    EXTRA_BUTTON = KeyboardButton.BACK_BUTTON
    BUTTON_ROW_SIZE = 1
