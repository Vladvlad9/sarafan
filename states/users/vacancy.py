from aiogram.dispatcher.filters.state import StatesGroup, State


class AddVacancy(StatesGroup):
    CitizenshipId = State()
    CityId = State()
    WorkExperienceId = State()
    AgeId = State()
    KnowledgeOfEnglish = State()
    Position = State()
    SubPosition = State()
    Approve = State()


class EditVacancy(StatesGroup):
    CitizenshipId = State()
    CityId = State()
    WorkExperienceId = State()
    AgeId = State()
    KnowledgeOfEnglish = State()
    Position = State()
    SubPosition = State()


class InviteCandidate(StatesGroup):
    Text = State()
    Approve = State()
