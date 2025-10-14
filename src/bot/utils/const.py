from keyboards.inline import KeyboardButton


class CallbackName:
    SETTINGS_CALLBACK = "get_settings"
    BACK_CALLBACK = "back"
    CANCEL_CALLBACK = "cancel"
    SUPPLY_PLANNING_CALLBACK = "plan_supplies"
    SUPPLY_PLANNING_SETTINGS_CALLBACK = "supply_thresholds_settings"
    REFRESH_SUPPLY_SETTINGS = "refresh_settings"


class MenuSectionId:
    MAIN_MENU = 1
    SETTINGS = 2
    SUPPLY_PLANNING = 3


class MainMenuKeyboard:
    EXTRA_BUTTON = KeyboardButton.CANCEL_BUTTON
    BUTTON_ROW_SIZE = 1


class SettingsMenuKeyboard:
    EXTRA_BUTTON = KeyboardButton.BACK_BUTTON
    REFRESH_BUTTON = KeyboardButton.REFRESH_BUTTON
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


class SupplySettings:
    # Пороги для количества товаров в пути
    MIN_TO_CLIENT_THRESHOLD = "min_to_client_threshold"
    MAX_TO_CLIENT_LOW = "max_to_client_low"
    MAX_TO_CLIENT_MEDIUM = "max_to_client_medium"

    # Пороги для остатков на складе
    WAREHOUSE_REMAINS_THRESHOLD = "warehouse_remains_threshold"

    # Пороги для общего количества
    TOTAL_THRESHOLD = "total_threshold"

    # Количества для заказа
    QUANTITY_SMALL = "quantity_small"
    QUANTITY_MEDIUM = "quantity_medium"
    QUANTITY_LARGE = "quantity_large"
