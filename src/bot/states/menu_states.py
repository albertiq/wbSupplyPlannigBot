from aiogram.fsm.state import State, StatesGroup


class MenuStates(StatesGroup):
    start = State()
    settings = State()
    warehouses = State()
