from aiogram.dispatcher.filters.state import State, StatesGroup


class AddMailingFSM(StatesGroup):
    AddPhoto = State()
    AddText = State()
    Approve = State()
