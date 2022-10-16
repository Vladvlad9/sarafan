from aiogram.dispatcher.filters.state import StatesGroup, State


class EditRegister(StatesGroup):
    DateOfBirth = State()
    PhoneNumber = State()
    InstagramUrl = State()

    Name = State()
    Surname = State()
    Patronymic = State()

    RecentJob = State()

    ApplicantFormId = State()

    Examination = State()
    ExaminationId = State()

    NewRecentJob = State()