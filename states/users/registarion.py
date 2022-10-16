from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegister(StatesGroup):
    DateOfBirth = State()
    CitizenshipId = State()
    isMarried = State()
    CityId = State()
    WorkExperienceId = State()
    PhoneNumber = State()
    Username = State()
    InstagramUrl = State()
    KnowledgeOfEnglish = State()
    PositionId = State()

    Name = State()
    Surname = State()
    Patronymic = State()

    FIO = State()

    Subpositions = State()

    RecentJob = State()
    AddRecentJob = State()
    NewRecentJob = State()

    Canceled = State()

    User_id = State()
    BackaddRecentJob = State()