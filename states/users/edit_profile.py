from aiogram.dispatcher.filters.state import StatesGroup, State


class EditProfile(StatesGroup):
    DateOfBirth = State()
    PhoneNumber = State()
    InstagramUrl = State()

    Name = State()
    Surname = State()
    Patronymic = State()

    RecentJob = State()
    RecentJobEdit = State()

    ApplicantFormId = State()

    Examination = State()
    ExaminationId = State()