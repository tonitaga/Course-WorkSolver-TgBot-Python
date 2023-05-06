from aiogram.dispatcher.filters.state import State, StatesGroup


class BroachState(StatesGroup):
    broach_data = State()