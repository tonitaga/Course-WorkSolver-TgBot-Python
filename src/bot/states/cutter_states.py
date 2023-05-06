from aiogram.dispatcher.filters.state import State, StatesGroup


class CutterState(StatesGroup):
    cut_type = State()
    cut_data = State()