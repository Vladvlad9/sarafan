from aiogram.dispatcher.filters.state import State, StatesGroup


class AddCitizenshipFSM(StatesGroup):
    AddCitizenship = State()
    Approve = State()
