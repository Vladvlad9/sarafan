from aiogram.dispatcher.filters.state import State, StatesGroup


class AddWorkExperienceFSM(StatesGroup):
    AddWorkExperience = State()
    Approve = State()
