from aiogram.dispatcher.filters.state import State, StatesGroup


class AddPositionFSM(StatesGroup):
    AddPosition = State()
    Approve = State()


class AddSubPositionFSM(StatesGroup):
    AddSubPosition = State()
    Approve = State()
