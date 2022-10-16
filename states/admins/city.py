from aiogram.dispatcher.filters.state import State, StatesGroup


class AddCityFSM(StatesGroup):
    AddCity = State()
    Approve = State()
