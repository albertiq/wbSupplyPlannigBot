from keyboards.inline import KeyboardButton

GROUPED_WAREHOUSES = {
    "Москва": ("Коледино", "Подольск", "Электросталь", "Тула"),
    "Казань": ("Казань", "Самара (Новосемейкино)"),
}
WAREHOUSES_LIST = ("Москва", "Краснодар", "Казань", "Екатеринбург - Перспективный 12")


class CallbackName:
    SETTINGS_CALLBACK = "get_settings"
    BACK_CALLBACK = "back"
    CANCEL_CALLBACK = "cancel"
    SUPPLY_PLANNING_CALLBACK = "plan_supplies"


class MenuSectionId:
    MAIN_MENU = 1
    SETTINGS = 2
    SUPPLY_PLANNING = 3


class MainMenuKeyboard:
    EXTRA_BUTTON = KeyboardButton.CANCEL_BUTTON
    BUTTON_ROW_SIZE = 2


class SettingsMenuKeyboard:
    EXTRA_BUTTON = KeyboardButton.BACK_BUTTON
    BUTTON_ROW_SIZE = 1


class SupportMenuKeyboard:
    SUPPORT_BUTTON = KeyboardButton.SUPPORT_BUTTON


class ReportStatus:
    DONE = "done"
    PROCESSING = "processing"


class CreateReportConsts:
    CREATE_REPORT_SLEEP = 5
    CREATE_REPORT_TIMEOUT = 60


class WarehouseRemainsInfo:
    ON_THE_WAY_TO_CLIENT = "В пути до получателей"
    ON_THE_WAY_BACK = "В пути возвраты на склад WB"
    TOTAL_IN_WAREHOUSES = "Всего находится на складах"
