from aiogram.dispatcher.filters.state import State, StatesGroup


class AddAgeFSM(StatesGroup):
    AddAge = State()
    Approve = State()
