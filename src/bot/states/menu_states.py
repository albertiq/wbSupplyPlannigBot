from aiogram.fsm.state import State, StatesGroup


class MenuStates(StatesGroup):
    start = State()
    settings = State()
    supply_planning_settings = State()
    edit_supply_planning_setting = State()
