from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest
from crud import CRUDCitizenShip, CRUDCity, CRUDWorkExperience, CRUDPosition, CRUDUser, \
    CRUDVacancy, CRUDApplicantForm, CRUDRecentJob, CRUDEmployerReply, CRUDAge
from crud.applicant_reply import CRUDApplicantReply
from crud.english import CRUDEnglish
from enums import Roles
from loader import bot
from schemas import VacancySchema, UserSchema, EmployerReplySchema
from states.users import AddVacancy, EditVacancy, InviteCandidate
from config import CONFIG

employer_cb = CallbackData("employer", "action", "target", "id")


async def employer_ikb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Создать вакансию",
                    callback_data=employer_cb.new("add", "vacancy", 0)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Мои вакансии",
                    callback_data=employer_cb.new("show", "vacancies", 0)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отклики",
                    callback_data=employer_cb.new("show", "responses", 0)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Поддержка",
                    callback_data=employer_cb.new("show", "support", 0)
                )
            ]
        ]
    )
    return keyboard


async def list_citizenships_ikb(vacancy_id: int = None) -> InlineKeyboardMarkup:
    all_citizenships = await CRUDCitizenShip.get_all()
    if vacancy_id is None:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{citizenship.name}",
                    callback_data=employer_cb.new("get", "citizenship", citizenship.id)
                ),
            ]
            for citizenship in all_citizenships
        ]
        keyboards.append(
            [
                InlineKeyboardButton(text="Пропустить", callback_data=employer_cb.new("miss", "miss_citizenship", 0))
            ]
        )
        keyboards.append(
            [
                InlineKeyboardButton(text="Назад", callback_data=employer_cb.new("cancel", "back", 0))
            ]
        )
    else:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{citizenship.name}",
                    callback_data=employer_cb.new("edit_vacancy", "citizenship", f"{vacancy_id}_{citizenship.id}")
                ),
            ]
            for citizenship in all_citizenships
        ]
        keyboards.append(
            [
                InlineKeyboardButton(
                    text="Неважно",
                    callback_data=employer_cb.new("edit_vacancy", "citizenship", f"{vacancy_id}_None"))
            ]
        )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def list_cities_ikb(vacancy_id: int = None) -> InlineKeyboardMarkup:
    all_cities = await CRUDCity.get_all()
    if vacancy_id is None:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{city.name}",
                    callback_data=employer_cb.new("get", "city", city.id)
                )
            ]
            for city in all_cities
        ]
        keyboards.append(
            [
                InlineKeyboardButton(text="Пропустить", callback_data=employer_cb.new("miss", "miss_city", 0))
            ]
        )
        keyboards.append(
            [
                InlineKeyboardButton(text="Назад", callback_data=employer_cb.new("back_citizenships", "back", 0))
            ]
        )
    else:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{city.name}",
                    callback_data=employer_cb.new("edit_vacancy", "city", f"{vacancy_id}_{city.id}")
                )
            ]
            for city in all_cities
        ]
        keyboards.append(
            [
                InlineKeyboardButton(
                    text="Неважно",
                    callback_data=employer_cb.new("edit_vacancy", "city", f"{vacancy_id}_None"))
            ]
        )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def list_ages_ikb(vacancy_id: int = None) -> InlineKeyboardMarkup:
    all_ages = await CRUDAge.get_all()
    if vacancy_id is None:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{age.name}",
                    callback_data=employer_cb.new("get", "age", age.id)
                )
            ]
            for age in all_ages
        ]
        keyboards.append(
            [
                InlineKeyboardButton(text="Назад", callback_data=employer_cb.new("back_work_experiences", "back", 0))
            ]
        )
    else:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{age.name}",
                    callback_data=employer_cb.new("edit_vacancy", "age", f"{vacancy_id}_{age.id}")
                )
            ]
            for age in all_ages
        ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def list_work_experiences_ikb(vacancy_id: int = None) -> InlineKeyboardMarkup:
    all_work_experience = await CRUDWorkExperience.get_all()
    if vacancy_id is None:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{work_experience.name}",
                    callback_data=employer_cb.new("get", "work_experience", work_experience.id)
                )
            ]
            for work_experience in all_work_experience
        ]
        keyboards.append(
            [
                InlineKeyboardButton(text="Пропустить",
                                     callback_data=employer_cb.new("miss", "miss_work_experience", 0))
            ]
        )
        keyboards.append(
            [
                InlineKeyboardButton(text="Назад", callback_data=employer_cb.new("back_cities", "back", 0))
            ]
        )
    else:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{work_experience.name}",
                    callback_data=employer_cb.new("edit_vacancy",
                                                  "work_experience",
                                                  f"{vacancy_id}_{work_experience.id}")
                )
            ]
            for work_experience in all_work_experience
        ]
        keyboards.append(
            [
                InlineKeyboardButton(
                    text="Неважно",
                    callback_data=employer_cb.new("edit_vacancy", "work_experience", f"{vacancy_id}_None"))
            ]
        )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def knowledge_of_english_ikb(vacancy_id: int = None) -> InlineKeyboardMarkup:
    all_english = await CRUDEnglish.get_all()
    if vacancy_id is None:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{english.name}",
                    callback_data=employer_cb.new("get", "knowledgeofenglish", english.id)
                )
            ]
            for english in all_english
        ]
        keyboards.append(
            [
                InlineKeyboardButton(text="Пропустить",
                                     callback_data=employer_cb.new("miss", "miss_knowledge_of_english", 0))
            ]
        )
        keyboards.append(
            [
                InlineKeyboardButton(text="Назад", callback_data=employer_cb.new("back_ages", "back", 0))
            ]
        )
    else:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{english.name}",
                    callback_data=employer_cb.new("edit_vacancy", "knowledgeofenglish", f"{vacancy_id}_{english.id}")
                )
            ]
            for english in all_english
        ]
        keyboards.append(
            [
                InlineKeyboardButton(
                    text="Неважно",
                    callback_data=employer_cb.new("edit_vacancy", "knowledgeofenglish", f"{vacancy_id}_None"))
            ]
        )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def list_positions_ikb(vacancy_id: int = None, subpositions_id: list = None) -> InlineKeyboardMarkup:
    all_positions = await CRUDPosition.get_all_positions()
    if vacancy_id is None:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{position.name}",
                    callback_data=employer_cb.new("get", "positions", position.id)
                )
            ]
            for position in all_positions
        ]
        if subpositions_id:
            keyboards.append([InlineKeyboardButton(
                text="Готово!",
                callback_data=employer_cb.new("get", "pre_approve_add_vacancy", 0))])
        keyboards.append(
            [
                InlineKeyboardButton(text="Назад", callback_data=employer_cb.new("back_english", "back", 0))
            ]
        )
    else:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{position.name}",
                    callback_data=employer_cb.new("edit_vacancy", "positions", f"{vacancy_id}_{position.id}")
                )
            ]
            for position in all_positions
        ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def list_subpositions_ikb(position_id: int,
                                vacancy_id: int = None,
                                subpositions_id: list = None) -> InlineKeyboardMarkup:
    all_subpositions = await CRUDPosition.get_all_subpositions(position_id=position_id)
    if vacancy_id is None:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=subposition.name if subposition.id not in subpositions_id else f"{subposition.name} ✅",
                    callback_data=employer_cb.new("get", "subpositions", subposition.id)
                )
            ]
            for subposition in all_subpositions
        ]
        if subpositions_id:
            keyboards.append([InlineKeyboardButton(
                text="Готово!",
                callback_data=employer_cb.new("get", "pre_approve_add_vacancy", 0))])
        keyboards.append(
            [
                InlineKeyboardButton(text="Назад", callback_data=employer_cb.new("back_positions", "back", 0))
            ]
        )
    else:
        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{subposition.name}",
                    callback_data=employer_cb.new("edit_vacancy", "subpositions", f"{vacancy_id}_{subposition.id}")
                )
            ]
            for subposition in all_subpositions
        ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def approve_add_vacancy(position_id: int = None) -> InlineKeyboardMarkup:
    keyboards = [
        [
            InlineKeyboardButton(
                text=f"Да",
                callback_data=employer_cb.new("get", "approve_add_vacancy", 0)
            ),
            InlineKeyboardButton(
                text=f"Нет",
                callback_data=employer_cb.new("get", "revoke_add_vacancy", 0)
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data=employer_cb.new("back_subpositions", "back", position_id)
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def vacancies_iter_ikb(action: str,
                             target: str,
                             user_id: int,
                             page: int = 0) -> InlineKeyboardMarkup:
    vacancies = await CRUDVacancy.get_vacancies_employer(user_id=user_id)

    vacancies_count = len(vacancies)

    prev_page: int
    next_page: int

    if page == 0:
        prev_page = vacancies_count - 1
        next_page = page + 1
    elif page == vacancies_count - 1:
        prev_page = page - 1
        next_page = 0
    else:
        prev_page = page - 1
        next_page = page + 1

    back_ikb = InlineKeyboardButton("Назад", callback_data=employer_cb.new("show_menu", "employer", 0))
    prev_page_ikb = InlineKeyboardButton("←", callback_data=employer_cb.new(action, target, prev_page))
    next_page_ikb = InlineKeyboardButton("→", callback_data=employer_cb.new(action, target, next_page))

    vacancies_ikb = InlineKeyboardButton("☰", callback_data=employer_cb.new("show",
                                                                            "vacancy_menu",
                                                                            vacancies[page].id))
    if vacancies_count == 1:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    vacancies_ikb
                ],
                [
                    back_ikb
                ]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    prev_page_ikb,
                    next_page_ikb,
                    vacancies_ikb,
                ],
                [back_ikb]
            ]
        )


async def responses_iter_ikb(action: str,
                             target: str,
                             user_id: int,
                             page: int = 0) -> InlineKeyboardMarkup:
    my_vacancies_id = [vacancy.id for vacancy in
                       await CRUDVacancy.get_vacancies_employer(user_id=user_id)]
    responses = []
    for vacancy_id in my_vacancies_id:
        response = await CRUDApplicantReply.get(vacancy_id=vacancy_id)
        if response:
            responses.append(response)

    responses_count = len(responses)

    prev_page: int
    next_page: int

    if page == 0:
        prev_page = responses_count - 1
        next_page = page + 1
    elif page == responses_count - 1:
        prev_page = page - 1
        next_page = 0
    else:
        prev_page = page - 1
        next_page = page + 1

    back_ikb = InlineKeyboardButton("Назад", callback_data=employer_cb.new("show_menu", "employer", 0))
    prev_page_ikb = InlineKeyboardButton("←", callback_data=employer_cb.new(action, target, prev_page))
    next_page_ikb = InlineKeyboardButton("→", callback_data=employer_cb.new(action, target, next_page))

    responses_ikb = InlineKeyboardButton("☰", callback_data=employer_cb.new("show",
                                                                            "responses_menu",
                                                                            responses[page].id))
    if responses_count == 1:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    responses_ikb
                ],
                [
                    back_ikb
                ]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    prev_page_ikb,
                    next_page_ikb,
                    responses_ikb,
                ],
                [back_ikb]
            ]
        )


async def candidates_iter_ikb(action: str,
                              target: str,
                              vacancy_id: int,
                              page: int = 0) -> InlineKeyboardMarkup:
    candidates: list = []
    for i in await CRUDApplicantForm.get_all(is_published=True):
        if await CRUDVacancy.get(vacancy_id=vacancy_id, position_id=i.position_id):
            candidates.append(i)

    candidates_count = len(candidates)

    prev_page: int
    next_page: int

    if page == 0:
        prev_page = candidates_count - 1
        next_page = page + 1
    elif page == candidates_count - 1:
        prev_page = page - 1
        next_page = 0
    else:
        prev_page = page - 1
        next_page = page + 1

    back_ikb = InlineKeyboardButton("Назад",
                                    callback_data=employer_cb.new("show", "vacancy_menu", vacancy_id))
    prev_page_ikb = InlineKeyboardButton("←",
                                         callback_data=employer_cb.new(action, target,
                                                                       f"{prev_page}_{vacancy_id}"))
    next_page_ikb = InlineKeyboardButton("→",
                                         callback_data=employer_cb.new(action, target,
                                                                       f"{next_page}_{vacancy_id}"))

    responses_ikb = InlineKeyboardButton("Пригласить",
                                         callback_data=employer_cb.new("invite", target,
                                                                       f"{candidates[page].user_id}_{vacancy_id}"))
    if candidates_count == 1:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    responses_ikb
                ],
                [
                    back_ikb
                ]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    prev_page_ikb,
                    next_page_ikb,
                    responses_ikb,
                ],
                [back_ikb]
            ]
        )


async def details_vacancy_ikb(vacancy_id: int = 0) -> InlineKeyboardMarkup:
    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
    if vacancy.is_published:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Кандидаты",
                                      callback_data=employer_cb.new("show", "candidates", vacancy_id))],
                [InlineKeyboardButton(text="Редактировать",
                                      callback_data=employer_cb.new("edit_vacancy", "vacancy_menu", vacancy_id))],
                [InlineKeyboardButton(text="Скрыть",
                                      callback_data=employer_cb.new("hide_vacancy", "vacancy_menu", vacancy_id))],
                [InlineKeyboardButton(text="Удалить",
                                      callback_data=employer_cb.new("delete_vacancy", "vacancy_menu", vacancy_id))],
                [InlineKeyboardButton(text="Назад",
                                      callback_data=employer_cb.new("show", "vacancies", vacancy_id))]
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Кандидаты",
                                      callback_data=employer_cb.new("show", "candidates", vacancy_id))],
                [InlineKeyboardButton(text="Редактировать",
                                      callback_data=employer_cb.new("edit_vacancy", "vacancy_menu", vacancy_id))],
                [InlineKeyboardButton(text="Опубликовать",
                                      callback_data=employer_cb.new("publish_vacancy", "vacancy_menu", vacancy_id))],
                [InlineKeyboardButton(text="Удалить",
                                      callback_data=employer_cb.new("delete_vacancy", "vacancy_menu", vacancy_id))],
                [InlineKeyboardButton(text="Назад",
                                      callback_data=employer_cb.new("show", "vacancies", vacancy_id))]
            ]
        )
    return keyboard


async def details_response_ikb(response_id: int = 0) -> InlineKeyboardMarkup:
    response = await CRUDApplicantReply.get(applicant_reply_id=response_id)
    chat = await bot.get_chat(
        chat_id=response.user_id  # сделать динамическим
    )
    button_url = chat.user_url
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Связаться",
                                  callback_data=employer_cb.new("contact_to_applicant",
                                                                "responses_menu", response_id),
                                  url=button_url, )],
            [InlineKeyboardButton(text="Одобрить",
                                  callback_data=employer_cb.new("approve_response",
                                                                "responses_menu", response_id))],
            [InlineKeyboardButton(text="Отклонить",
                                  callback_data=employer_cb.new("reject_response",
                                                                "responses_menu", response_id))],
            [InlineKeyboardButton(text="Назад",
                                  callback_data=employer_cb.new("show",
                                                                "responses", response_id))]
        ]
    )
    return keyboard


async def edit_vacancy_ikb(vacancy_id: int = 0) -> InlineKeyboardMarkup:
    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)

    if vacancy.citizenship_id is None:
        citizenship = "Неважно"
    else:
        citizenship_id = await CRUDCitizenShip.get(citizenship_id=vacancy.citizenship_id)
        citizenship = citizenship_id.name

    if vacancy.city_id is None:
        city = "Неважно"
    else:
        city_id = await CRUDCity.get(city_id=vacancy.city_id)
        city = city_id.name

    if vacancy.work_experience_id is None:
        work_experience = "Неважно"
    else:
        work_experience_id = await CRUDWorkExperience.get(
            work_experience_id=vacancy.work_experience_id)
        work_experience = work_experience_id.name

    if vacancy.english_id is None:
        english = "Неважно"
    else:
        english_id = await CRUDEnglish.get(english_id=vacancy.english_id)
        english = english_id.name

    age = await CRUDAge.get(age_id=vacancy.age_id)
    subposition = await CRUDPosition.get(position_id=vacancy.position_id)
    position = await CRUDPosition.get(position_id=subposition.parent_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"Гражданство - {citizenship}",
                                     callback_data=employer_cb.new("edit_citizenship", "edit_vacancy", vacancy_id))
            ],
            [
                InlineKeyboardButton(text=f"Город - {city}",
                                     callback_data=employer_cb.new("edit_city", "edit_vacancy", vacancy_id))
            ],
            [
                InlineKeyboardButton(text=f"Стаж - {work_experience}",
                                     callback_data=employer_cb.new("edit_work_experience", "edit_vacancy", vacancy_id))
            ],
            [
                InlineKeyboardButton(text=f"Возраст - {age.name}",
                                     callback_data=employer_cb.new("edit_age", "edit_vacancy", vacancy_id))
            ],
            [
                InlineKeyboardButton(text=f"Специальность - {subposition.name} должности {position.name} ",
                                     callback_data=employer_cb.new("edit_position", "edit_vacancy", vacancy_id))
            ],
            [
                InlineKeyboardButton(text=f"Английский - {english}",
                                     callback_data=employer_cb.new("edit_knowledge_of_english",
                                                                   "edit_vacancy", vacancy_id))
            ],
            [
                InlineKeyboardButton(text="Назад",
                                     callback_data=employer_cb.new("show", "vacancy_menu", vacancy_id))
            ],
        ]
    )
    return keyboard


async def back_in_main_menu_ikb() -> InlineKeyboardMarkup:
    keyboards = [
        [
            InlineKeyboardButton(text="Назад", callback_data=employer_cb.new("show_menu", "employer", 0))
        ]
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def approve_invite_candidate() -> InlineKeyboardMarkup:
    keyboards = [
        [
            InlineKeyboardButton(text="ДА", callback_data=employer_cb.new("approve", "candidates", 0)),
            InlineKeyboardButton(text="НЕТ", callback_data=employer_cb.new("incorrect", "candidates", 0))
        ]
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


class Employer:

    @staticmethod
    async def process(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            data = employer_cb.parse(callback_data=callback.data)
            if state:
                # Создание вакансии
                if await state.get_state() == "AddVacancy:CitizenshipId":
                    if data.get("action") == "get":
                        if data.get("target") == "citizenship":
                            await state.update_data(citizenship_id=data["id"])
                            await AddVacancy.CityId.set()
                            await callback.message.edit_text(
                                text="Выберите город, который должен быть у соискателя:",
                                reply_markup=await list_cities_ikb()
                            )
                    if data.get("action") == "miss":
                        if data.get("target") == "miss_citizenship":
                            await state.update_data(citizenship_id=None)
                            await AddVacancy.CityId.set()
                            await callback.message.edit_text(
                                text="Выберите город, который должен быть у соискателя:",
                                reply_markup=await list_cities_ikb()
                            )
                elif await state.get_state() == "AddVacancy:CityId":
                    if data.get("action") == "get":
                        if data.get("target") == "city":
                            await state.update_data(city_id=data["id"])
                            await AddVacancy.WorkExperienceId.set()
                            await callback.message.edit_text(
                                text="Выберите опыт работы, который должен быть у соискателя:",
                                reply_markup=await list_work_experiences_ikb()
                            )
                    if data.get("action") == "miss":
                        if data.get("target") == "miss_city":
                            await state.update_data(city_id=None)
                            await AddVacancy.WorkExperienceId.set()
                            await callback.message.edit_text(
                                text="Выберите опыт работы, который должен быть у соискателя:",
                                reply_markup=await list_work_experiences_ikb()
                            )
                elif await state.get_state() == "AddVacancy:WorkExperienceId":
                    if data.get("action") == "get":
                        if data.get("target") == "work_experience":
                            await state.update_data(work_experience_id=data["id"])
                            await AddVacancy.AgeId.set()
                            await callback.message.edit_text(
                                text="Выберите желаемый возраст соискателя:",
                                reply_markup=await list_ages_ikb()
                            )
                    if data.get("action") == "miss":
                        if data.get("target") == "miss_work_experience":
                            await state.update_data(work_experience_id=None)
                            await AddVacancy.AgeId.set()
                            await callback.message.edit_text(
                                text="Выберите желаемый возраст соискателя:",
                                reply_markup=await list_ages_ikb()
                            )
                elif await state.get_state() == "AddVacancy:AgeId":
                    if data.get("action") == "get":
                        if data.get("target") == "age":
                            await state.update_data(age_id=data["id"])
                            await AddVacancy.KnowledgeOfEnglish.set()
                            await callback.message.edit_text(
                                text="Выберите уровень знания английского у соискателя:",
                                reply_markup=await knowledge_of_english_ikb()
                            )
                elif await state.get_state() == "AddVacancy:KnowledgeOfEnglish":
                    if data.get("action") == "get":
                        if data.get("target") == "knowledgeofenglish":
                            await state.update_data(english_id=data["id"])
                            subpositions = []
                            await state.update_data(subpositions=subpositions)
                            await AddVacancy.Position.set()
                            await callback.message.edit_text(
                                text="Выберите должность:",
                                reply_markup=await list_positions_ikb(subpositions_id=subpositions)
                            )
                    if data.get("action") == "miss":
                        if data.get("target") == "miss_knowledge_of_english":
                            await state.update_data(english_id=None)
                            subpositions = []
                            await state.update_data(subpositions=subpositions)
                            await AddVacancy.Position.set()
                            await callback.message.edit_text(
                                text="Выберите должность:",
                                reply_markup=await list_positions_ikb(subpositions_id=subpositions)
                            )
                elif await state.get_state() == "AddVacancy:Position":
                    if data.get("action") == "get":
                        if data.get("target") == "positions":
                            state_data: dict = await state.get_data()
                            position_id = int(data.get("id"))
                            position = await CRUDPosition.get(position_id=position_id)
                            await state.update_data(parent_position_id=position_id)
                            await AddVacancy.SubPosition.set()
                            await callback.message.edit_text(
                                text=f"Выберите специальность для должности {position.name}:",
                                reply_markup=await list_subpositions_ikb(position_id=position_id,
                                                                         subpositions_id=state_data["subpositions"])
                            )
                    if data.get("target") == "pre_approve_add_vacancy":
                        state_data: dict = await state.get_data()
                        i = list(state_data["subpositions"])[0]
                        if state_data["citizenship_id"] is None:
                            citizenship = "Неважно"
                        else:
                            citizenship_id = await CRUDCitizenShip.get(
                                citizenship_id=int(state_data["citizenship_id"])
                            )
                            citizenship = citizenship_id.name
                        if state_data["city_id"] is None:
                            city = "Неважно"
                        else:
                            city_id = await CRUDCity.get(
                                city_id=int(state_data["city_id"])
                            )
                            city = city_id.name
                        if state_data["work_experience_id"] is None:
                            work_experience = "Неважно"
                        else:
                            work_experience_id = await CRUDWorkExperience.get(
                                work_experience_id=int(state_data["work_experience_id"])
                            )
                            work_experience = work_experience_id.name
                        if state_data["english_id"] is None:
                            english = "Неважно"
                        else:
                            english_id = await CRUDEnglish.get(english_id=int(state_data["english_id"]))
                            english = english_id.name
                        age = await CRUDAge.get(
                            age_id=int(state_data["age_id"])
                        )
                        subposition = await CRUDPosition.get(
                            position_id=int(i)
                        )
                        position = await CRUDPosition.get(
                            position_id=subposition.parent_id
                        )
                        await AddVacancy.Approve.set()
                        text = f"Гражданство: <b>{citizenship}</b>\n" \
                               f"Город: <b>{city}</b>\n" \
                               f"Опыт работы: <b>{work_experience}</b>\n" \
                               f"Возраст: <b>{age.name}</b>\n" \
                               f"Знание английского: <b>{english}</b>\n" \
                               f"Специальность <b>{subposition.name}</b>" \
                               f" для должности <b>{position.name}</b>\n"
                        await callback.message.edit_text(
                            text="Проверьте правильность введенных данных:\n\n" + text,
                            reply_markup=await approve_add_vacancy(position_id=position.id)
                        )
                elif await state.get_state() == "AddVacancy:SubPosition":
                    if data.get("action") == "get":
                        if data.get("target") == "subpositions":
                            state_data: dict = await state.get_data()
                            subpositions = list(state_data["subpositions"])
                            if int(data.get("id")) in subpositions:
                                subpositions.remove(int(data.get("id")))
                            else:
                                subpositions.append(int(data.get("id")))
                            await state.update_data(subpositions=subpositions)
                            position = await CRUDPosition.get(position_id=state_data["parent_position_id"])
                            await state.update_data(user_id=callback.from_user.id)
                            await AddVacancy.SubPosition.set()
                            await callback.message.edit_text(
                                text=f"Выберите специальность для должности {position.name}:",
                                reply_markup=await list_subpositions_ikb(position_id=position.id,
                                                                         subpositions_id=subpositions)
                            )
                        if data.get("target") == "pre_approve_add_vacancy":
                            state_data: dict = await state.get_data()
                            i = list(state_data["subpositions"])[0]
                            if state_data["citizenship_id"] is None:
                                citizenship = "Неважно"
                            else:
                                citizenship_id = await CRUDCitizenShip.get(
                                    citizenship_id=int(state_data["citizenship_id"])
                                )
                                citizenship = citizenship_id.name
                            if state_data["city_id"] is None:
                                city = "Неважно"
                            else:
                                city_id = await CRUDCity.get(
                                    city_id=int(state_data["city_id"])
                                )
                                city = city_id.name
                            if state_data["work_experience_id"] is None:
                                work_experience = "Неважно"
                            else:
                                work_experience_id = await CRUDWorkExperience.get(
                                    work_experience_id=int(state_data["work_experience_id"])
                                )
                                work_experience = work_experience_id.name
                            if state_data["english_id"] is None:
                                english = "Неважно"
                            else:
                                english_id = await CRUDEnglish.get(english_id=int(state_data["english_id"]))
                                english = english_id.name
                            age = await CRUDAge.get(
                                age_id=int(state_data["age_id"])
                            )
                            subposition = await CRUDPosition.get(
                                position_id=int(i)
                            )
                            position = await CRUDPosition.get(
                                position_id=subposition.parent_id
                            )
                            await AddVacancy.Approve.set()
                            text = f"Гражданство: <b>{citizenship}</b>\n" \
                                   f"Город: <b>{city}</b>\n" \
                                   f"Опыт работы: <b>{work_experience}</b>\n" \
                                   f"Возраст: <b>{age.name}</b>\n" \
                                   f"Знание английского: <b>{english}</b>\n" \
                                   f"Специальность <b>{subposition.name}</b>" \
                                   f" для должности <b>{position.name}</b>\n"
                            await callback.message.edit_text(
                                text="Проверьте правильность введенных данных:\n\n" + text,
                                reply_markup=await approve_add_vacancy(position_id=position.id)
                            )
                elif await state.get_state() == "AddVacancy:Approve":
                    if data.get("action") == "get":
                        if data.get("target") == "approve_add_vacancy":
                            state_data: dict = await state.get_data()
                            if len(state_data["subpositions"]) > 0:
                                i = list(state_data["subpositions"])[0]
                                await state.update_data(position_id=int(i))
                                await state.update_data(is_published=True)
                                state_data: dict = await state.get_data()
                                await CRUDVacancy.add(vacancy=VacancySchema(**state_data))
                                await callback.answer(text="Вакансия была добавлена!")
                                subpositions = list(state_data["subpositions"])
                                del subpositions[0]
                                await state.update_data(subpositions=subpositions)
                                state_data: dict = await state.get_data()
                                if state_data["subpositions"]:
                                    val = list(state_data["subpositions"])[0]
                                    if state_data["citizenship_id"] is None:
                                        citizenship = "Неважно"
                                    else:
                                        citizenship_id = await CRUDCitizenShip.get(
                                            citizenship_id=int(state_data["citizenship_id"])
                                        )
                                        citizenship = citizenship_id.name
                                    if state_data["city_id"] is None:
                                        city = "Неважно"
                                    else:
                                        city_id = await CRUDCity.get(
                                            city_id=int(state_data["city_id"])
                                        )
                                        city = city_id.name
                                    if state_data["work_experience_id"] is None:
                                        work_experience = "Неважно"
                                    else:
                                        work_experience_id = await CRUDWorkExperience.get(
                                            work_experience_id=int(state_data["work_experience_id"])
                                        )
                                        work_experience = work_experience_id.name
                                    if state_data["english_id"] is None:
                                        english = "Неважно"
                                    else:
                                        english_id = await CRUDEnglish.get(
                                            english_id=int(state_data["english_id"]))
                                        english = english_id.name
                                    age = await CRUDAge.get(
                                        age_id=int(state_data["age_id"])
                                    )
                                    subposition = await CRUDPosition.get(
                                        position_id=int(val)
                                    )
                                    position = await CRUDPosition.get(
                                        position_id=subposition.parent_id
                                    )
                                    await AddVacancy.Approve.set()
                                    text = f"Гражданство: <b>{citizenship}</b>\n" \
                                           f"Город: <b>{city}</b>\n" \
                                           f"Опыт работы: <b>{work_experience}</b>\n" \
                                           f"Возраст: <b>{age.name}</b>\n" \
                                           f"Знание английского: <b>{english}</b>\n" \
                                           f"Специальность <b>{subposition.name}</b>" \
                                           f" для должности <b>{position.name}</b>\n"
                                    await callback.message.edit_text(
                                        text="Проверьте правильность введенных данных:\n\n" + text,
                                        reply_markup=await approve_add_vacancy(position_id=position.id)
                                    )
                                else:
                                    await state.finish()
                                    await callback.message.edit_text(
                                        text="Меню работодателя",
                                        reply_markup=await employer_ikb()
                                    )
                            else:
                                await state.finish()
                                await callback.message.edit_text(
                                    text="Меню работодателя",
                                    reply_markup=await employer_ikb()
                                )
                        if data.get("target") == "revoke_add_vacancy":
                            state_data: dict = await state.get_data()
                            if len(state_data["subpositions"]) > 0:
                                i = list(state_data["subpositions"])[0]
                                await state.update_data(position_id=int(i))
                                state_data: dict = await state.get_data()
                                await callback.answer(text="Добавление вакансии было отменено!")
                                subpositions = list(state_data["subpositions"])
                                del subpositions[0]
                                await state.update_data(subpositions=subpositions)
                                state_data: dict = await state.get_data()
                                if state_data["subpositions"]:
                                    val = list(state_data["subpositions"])[0]
                                    if state_data["citizenship_id"] is None:
                                        citizenship = "Неважно"
                                    else:
                                        citizenship_id = await CRUDCitizenShip.get(
                                            citizenship_id=int(state_data["citizenship_id"])
                                        )
                                        citizenship = citizenship_id.name
                                    if state_data["city_id"] is None:
                                        city = "Неважно"
                                    else:
                                        city_id = await CRUDCity.get(
                                            city_id=int(state_data["city_id"])
                                        )
                                        city = city_id.name
                                    if state_data["work_experience_id"] is None:
                                        work_experience = "Неважно"
                                    else:
                                        work_experience_id = await CRUDWorkExperience.get(
                                            work_experience_id=int(state_data["work_experience_id"])
                                        )
                                        work_experience = work_experience_id.name
                                    if state_data["english_id"] is None:
                                        english = "Неважно"
                                    else:
                                        english_id = await CRUDEnglish.get(
                                            english_id=int(state_data["english_id"]))
                                        english = english_id.name
                                    age = await CRUDAge.get(
                                        age_id=int(state_data["age_id"])
                                    )
                                    subposition = await CRUDPosition.get(
                                        position_id=int(val)
                                    )
                                    position = await CRUDPosition.get(
                                        position_id=subposition.parent_id
                                    )
                                    await AddVacancy.Approve.set()
                                    text = f"Гражданство: <b>{citizenship}</b>\n" \
                                           f"Город: <b>{city}</b>\n" \
                                           f"Опыт работы: <b>{work_experience}</b>\n" \
                                           f"Возраст: <b>{age.name}</b>\n" \
                                           f"Знание английского: <b>{english}</b>\n" \
                                           f"Специальность <b>{subposition.name}</b>" \
                                           f" для должности <b>{position.name}</b>\n"
                                    await callback.message.edit_text(
                                        text="Проверьте правильность введенных данных:\n\n" + text,
                                        reply_markup=await approve_add_vacancy(position_id=position.id)
                                    )
                                else:
                                    await state.finish()
                                    await callback.message.edit_text(
                                        text="Меню работодателя",
                                        reply_markup=await employer_ikb()
                                    )
                            else:
                                await state.finish()
                                await callback.message.edit_text(
                                    text="Меню работодателя",
                                    reply_markup=await employer_ikb()
                                )
                # Редактирование вакансии
                elif await state.get_state() == "EditVacancy:CitizenshipId":
                    if data.get("action") == "edit_vacancy":
                        if data.get("target") == "citizenship":
                            vacancy_id = int(data.get("id").split('_')[0])
                            if data.get("id").split('_')[1] == "None":
                                new_citizenship_id = None
                            else:
                                new_citizenship_id = int(data.get("id").split('_')[1])
                            vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                            vacancy.citizenship_id = new_citizenship_id
                            vacancy.date_created = datetime.now()
                            await CRUDVacancy.update(vacancy=vacancy)
                            await state.finish()
                            await callback.answer(text="Гражданство было изменено!")
                            await callback.message.edit_text(
                                text="Редактирование вакансии:",
                                reply_markup=await edit_vacancy_ikb(vacancy_id=vacancy_id)
                            )
                elif await state.get_state() == "EditVacancy:CityId":
                    if data.get("action") == "edit_vacancy":
                        if data.get("target") == "city":
                            vacancy_id = int(data.get("id").split('_')[0])
                            if data.get("id").split('_')[1] == "None":
                                new_city_id = None
                            else:
                                new_city_id = int(data.get("id").split('_')[1])
                            vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                            vacancy.city_id = new_city_id
                            vacancy.date_created = datetime.now()
                            await CRUDVacancy.update(vacancy=vacancy)
                            await state.finish()
                            await callback.answer(text="Город был изменен!")
                            await callback.message.edit_text(
                                text="Редактирование вакансии:",
                                reply_markup=await edit_vacancy_ikb(vacancy_id=vacancy_id)
                            )
                elif await state.get_state() == "EditVacancy:WorkExperienceId":
                    if data.get("action") == "edit_vacancy":
                        if data.get("target") == "work_experience":
                            vacancy_id = int(data.get("id").split('_')[0])
                            if data.get("id").split('_')[1] == "None":
                                new_work_experience_id = None
                            else:
                                new_work_experience_id = int(data.get("id").split('_')[1])
                            vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                            vacancy.work_experience_id = new_work_experience_id
                            vacancy.date_created = datetime.now()
                            await CRUDVacancy.update(vacancy=vacancy)
                            await state.finish()
                            await callback.answer(text="Опыт работы был изменен!")
                            await callback.message.edit_text(
                                text="Редактирование вакансии:",
                                reply_markup=await edit_vacancy_ikb(vacancy_id=vacancy_id)
                            )
                elif await state.get_state() == "EditVacancy:AgeId":
                    if data.get("action") == "edit_vacancy":
                        if data.get("target") == "age":
                            vacancy_id = int(data.get("id").split('_')[0])
                            new_age_id = int(data.get("id").split('_')[1])
                            vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                            vacancy.age_id = new_age_id
                            vacancy.date_created = datetime.now()
                            await CRUDVacancy.update(vacancy=vacancy)
                            await state.finish()
                            await callback.answer(text="Возраст был изменен!")
                            await callback.message.edit_text(
                                text="Редактирование вакансии:",
                                reply_markup=await edit_vacancy_ikb(vacancy_id=vacancy_id)
                            )
                elif await state.get_state() == "EditVacancy:KnowledgeOfEnglish":
                    if data.get("action") == "edit_vacancy":
                        if data.get("target") == "knowledgeofenglish":
                            vacancy_id = int(data.get("id").split('_')[0])
                            if data.get("id").split('_')[1] == "None":
                                new_english_id = None
                            else:
                                new_english_id = int(data.get("id").split('_')[1])
                            vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                            vacancy.english_id = new_english_id
                            vacancy.date_created = datetime.now()
                            await CRUDVacancy.update(vacancy=vacancy)
                            await state.finish()
                            await callback.answer(text="Знание английского было изменено!")
                            await callback.message.edit_text(
                                text="Редактирование вакансии:",
                                reply_markup=await edit_vacancy_ikb(vacancy_id=vacancy_id)
                            )
                elif await state.get_state() == "EditVacancy:Position":
                    if data.get("action") == "edit_vacancy":
                        if data.get("target") == "positions":
                            vacancy_id = int(data.get("id").split('_')[0])
                            new_position_id = int(data.get("id").split('_')[1])
                            await EditVacancy.SubPosition.set()
                            await callback.message.edit_text(
                                text="Изменение специальности:",
                                reply_markup=await list_subpositions_ikb(position_id=new_position_id,
                                                                         vacancy_id=vacancy_id)
                            )
                elif await state.get_state() == "EditVacancy:SubPosition":
                    if data.get("action") == "edit_vacancy":
                        if data.get("target") == "subpositions":
                            vacancy_id = int(data.get("id").split('_')[0])
                            new_subposition_id = int(data.get("id").split('_')[1])
                            vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                            vacancy.position_id = new_subposition_id
                            vacancy.date_created = datetime.now()
                            await CRUDVacancy.update(vacancy=vacancy)
                            await state.finish()
                            await callback.answer(text="Специальность была изменена!")
                            await callback.message.edit_text(
                                text="Редактирование вакансии:",
                                reply_markup=await edit_vacancy_ikb(vacancy_id=vacancy_id)
                            )
                # Приглашение кандидата
                elif await state.get_state() == "InviteCandidate:Approve":
                    if data.get("target") == "candidates":
                        if data.get("action") == "approve":
                            state_data: dict = await state.get_data()
                            candidate_id = state_data["candidate_id"]
                            vacancy_id = state_data["vacancy_id"]
                            await CRUDEmployerReply.add(employer_reply=EmployerReplySchema(candidate_id=candidate_id,
                                                                                           vacancy_id=vacancy_id
                                                                                           ))
                            text = state_data["text"]
                            chat = await bot.get_chat(
                                chat_id=callback.from_user.id
                            )
                            button_url = chat.user_url
                            await state.finish()
                            markup = types.InlineKeyboardMarkup()
                            markup.add(types.InlineKeyboardButton(text='Перейти к откравителю', url=button_url))
                            await bot.send_message(
                                chat_id=candidate_id,
                                text=f'{text}\n\n',
                                parse_mode="HTML",
                                reply_markup=markup
                            )
                            await callback.answer(text="Приглашение отправлено!")
                            await callback.message.delete()
                            await callback.message.answer(
                                text='<b>Меню работодателя:</b>',
                                reply_markup=await employer_ikb()
                            )
                        elif data.get("action") == "incorrect":
                            await InviteCandidate.Text.set()
                            await callback.answer(
                                text=f"Попробуйте еще раз!"
                            )
                            await callback.message.delete()
                            await callback.message.answer(
                                text="<b>Введите текст заново:</b>"
                            )
            # Меню работодателя
            if data.get("target") == "employer":
                if data.get("action") == "show_menu":
                    if await CRUDUser.get(user_id=callback.from_user.id) is None:
                        await CRUDUser.add(user=UserSchema(id=callback.from_user.id, role_id=Roles.Employer.value))
                    await callback.message.edit_text(
                        text="Меню работодателя",
                        reply_markup=await employer_ikb()
                    )
            # Добавление вакансии
            elif data.get("target") == "vacancy":
                if data.get("action") == "add":
                    await AddVacancy.CitizenshipId.set()
                    await callback.message.edit_text(
                        text="Выберите гражданство, которое должно быть у соискателя:",
                        reply_markup=await list_citizenships_ikb()
                    )
            # Вывод вакансий
            elif data.get("target") == "vacancies":
                if data.get("action") == "show":
                    vacancy = await CRUDVacancy.get(user_id=callback.from_user.id)
                    if vacancy:
                        if vacancy.citizenship_id:
                            citizenship_id = await CRUDCitizenShip.get(citizenship_id=vacancy.citizenship_id)
                            citizenship = citizenship_id.name
                        else:
                            citizenship = "Неважно"
                        if vacancy.city_id:
                            city_id = await CRUDCity.get(city_id=vacancy.city_id)
                            city = city_id.name
                        else:
                            city = "Неважно"
                        if vacancy.work_experience_id:
                            work_experience_id = await CRUDWorkExperience.get(
                                work_experience_id=vacancy.work_experience_id)
                            work_experience = work_experience_id.name
                        else:
                            work_experience = "Неважно"
                        if vacancy.english_id:
                            english_id = await CRUDEnglish.get(english_id=vacancy.english_id)
                            english = english_id.name
                        else:
                            english = "Неважно"
                        age = await CRUDAge.get(age_id=vacancy.age_id)
                        position = await CRUDPosition.get(position_id=vacancy.position_id)
                        date_created: str = f"{str(vacancy.date_created.day)}." \
                                            f"{str(vacancy.date_created.month)}." \
                                            f"{str(vacancy.date_created.year)}"
                        visible = '<b><u>опубликована!</u></b>' \
                            if vacancy.is_published else '<b><u>не опубликована!</u></b>'

                        text = f"Ваша вакансия <i>{visible}</i>\n\n" \
                               f"Гражданство: <b>{citizenship}</b>\n" \
                               f"Город: <b>{city}</b>\n" \
                               f"Опыт работы: <b>{work_experience}</b>\n" \
                               f"Возраст: <b>{age.name}</b>\n" \
                               f"Желаемая должность: <b>{position.name}</b>\n" \
                               f"Английский: <b>{english}</b>\n" \
                               f"Дата последнего изменения: <b>{date_created}</b>"

                        await callback.message.edit_text(
                            text='<b>Мои вакансии:</b>\n\n' + text,
                            reply_markup=await vacancies_iter_ikb(action="page",
                                                                  target="vacancies",
                                                                  user_id=callback.from_user.id)
                        )
                    else:
                        await callback.answer("На данный момент, созданых вами вакансий нет!")
                elif data.get("action") == "page":
                    page = int(data.get('id'))

                    vacancy = await CRUDVacancy.get_vacancies_employer(user_id=callback.from_user.id)

                    if vacancy[page].citizenship_id:
                        citizenship_id = await CRUDCitizenShip.get(citizenship_id=vacancy[page].citizenship_id)
                        citizenship = citizenship_id.name
                    else:
                        citizenship = "Неважно"
                    if vacancy[page].city_id:
                        city_id = await CRUDCity.get(city_id=vacancy[page].city_id)
                        city = city_id.name
                    else:
                        city = "Неважно"
                    age = await CRUDAge.get(age_id=vacancy[page].age_id)
                    if vacancy[page].work_experience_id:
                        work_experience_id = await CRUDWorkExperience.get(
                            work_experience_id=vacancy[page].work_experience_id)
                        work_experience = work_experience_id.name
                    else:
                        work_experience = "Неважно"
                    position = await CRUDPosition.get(position_id=vacancy[page].position_id)
                    if vacancy[page].english_id:
                        english_id = await CRUDEnglish.get(english_id=vacancy[page].english_id)
                        english = english_id.name
                    else:
                        english = "Неважно"
                    date_created: str = f"{str(vacancy[page].date_created.day)}." \
                                        f"{str(vacancy[page].date_created.month)}." \
                                        f"{str(vacancy[page].date_created.year)}"
                    visible = '<b><u>опубликована!</u></b>' \
                        if vacancy[page].is_published else '<b><u>не опубликована!</u></b>'

                    text = f"Ваша вакансия <i>{visible}</i>\n\n" \
                           f"Гражданство: <b>{citizenship}</b>\n" \
                           f"Город: <b>{city}</b>\n" \
                           f"Опыт работы: <b>{work_experience}</b>\n" \
                           f"Возраст: <b>{age.name}</b>\n" \
                           f"Желаемая должность: <b>{position.name}</b>\n" \
                           f"Английский: <b>{english}</b>\n" \
                           f"Дата последнего изменения: <b>{date_created}</b>"

                    await callback.message.edit_text(
                        text='<b>Мои вакансии:</b>\n\n' + text,
                        reply_markup=await vacancies_iter_ikb(action="page",
                                                              target="vacancies",
                                                              page=int(page),
                                                              user_id=callback.from_user.id)
                    )
            # Меню вакансии
            elif data.get("target") == "vacancy_menu":
                if data.get("action") == "show":
                    vacancy_id = int(data.get('id'))
                    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)

                    if vacancy.citizenship_id:
                        citizenship_id = await CRUDCitizenShip.get(citizenship_id=vacancy.citizenship_id)
                        citizenship = citizenship_id.name
                    else:
                        citizenship = "Неважно"
                    if vacancy.city_id:
                        city_id = await CRUDCity.get(city_id=vacancy.city_id)
                        city = city_id.name
                    else:
                        city = "Неважно"
                    if vacancy.work_experience_id:
                        work_experience_id = await CRUDWorkExperience.get(
                            work_experience_id=vacancy.work_experience_id)
                        work_experience = work_experience_id.name
                    else:
                        work_experience = "Неважно"
                    if vacancy.english_id:
                        english_id = await CRUDEnglish.get(english_id=vacancy.english_id)
                        english = english_id.name
                    else:
                        english = "Неважно"

                    age = await CRUDAge.get(age_id=vacancy.age_id)
                    position = await CRUDPosition.get(position_id=vacancy.position_id)
                    date_created: str = f"{str(vacancy.date_created.day)}." \
                                        f"{str(vacancy.date_created.month)}." \
                                        f"{str(vacancy.date_created.year)}"
                    visible = '<b><u>опубликована!</u></b>' \
                        if vacancy.is_published else '<b><u>не опубликована!</u></b>'

                    text = f"Ваша вакансия <i>{visible}</i>\n\n" \
                           f"Гражданство: <b>{citizenship}</b>\n" \
                           f"Город: <b>{city}</b>\n" \
                           f"Опыт работы: <b>{work_experience}</b>\n" \
                           f"Возраст: <b>{age.name}</b>\n" \
                           f"Желаемая должность: <b>{position.name}</b>\n" \
                           f"Английский: <b>{english}</b>\n" \
                           f"Дата последнего изменения: <b>{date_created}</b>"
                    await callback.message.edit_text(
                        text='<b>Моя вакансия:</b>\n\n' + text,
                        reply_markup=await details_vacancy_ikb(vacancy_id=vacancy_id)
                    )
                elif data.get("action") == "delete_vacancy":
                    vacancy_id = int(data.get('id'))
                    await CRUDVacancy.delete(vacancy_id=vacancy_id)
                    await callback.answer(text="Вакансия была удалена!")
                    await callback.message.edit_text(
                        text="Меню работодателя",
                        reply_markup=await employer_ikb()
                    )
                elif data.get("action") == "publish_vacancy":
                    vacancy_id = int(data.get('id'))
                    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                    vacancy.is_published = True
                    vacancy.date_created = datetime.now()
                    await CRUDVacancy.update(vacancy=vacancy)
                    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                    if vacancy.citizenship_id:
                        citizenship_id = await CRUDCitizenShip.get(citizenship_id=vacancy.citizenship_id)
                        citizenship = citizenship_id.name
                    else:
                        citizenship = "Неважно"
                    if vacancy.city_id:
                        city_id = await CRUDCity.get(city_id=vacancy.city_id)
                        city = city_id.name
                    else:
                        city = "Неважно"
                    if vacancy.work_experience_id:
                        work_experience_id = await CRUDWorkExperience.get(
                            work_experience_id=vacancy.work_experience_id)
                        work_experience = work_experience_id.name
                    else:
                        work_experience = "Неважно"
                    if vacancy.english_id:
                        english_id = await CRUDEnglish.get(english_id=vacancy.english_id)
                        english = english_id.name
                    else:
                        english = "Неважно"
                    age = await CRUDAge.get(age_id=vacancy.age_id)
                    position = await CRUDPosition.get(position_id=vacancy.position_id)
                    date_created: str = f"{str(vacancy.date_created.day)}." \
                                        f"{str(vacancy.date_created.month)}." \
                                        f"{str(vacancy.date_created.year)}"
                    visible = '<b><u>опубликована!</u></b>' \
                        if vacancy.is_published else '<b><u>не опубликована!</u></b>'

                    text = f"Ваша вакансия <i>{visible}</i>\n\n" \
                           f"Гражданство: <b>{citizenship}</b>\n" \
                           f"Город: <b>{city}</b>\n" \
                           f"Опыт работы: <b>{work_experience}</b>\n" \
                           f"Возраст: <b>{age.name}</b>\n" \
                           f"Желаемая должность: <b>{position.name}</b>\n" \
                           f"Английский: <b>{english}</b>\n" \
                           f"Дата последнего изменения: <b>{date_created}</b>"
                    await callback.answer(text="Вакансия была опубликована!")
                    await callback.message.edit_text(
                        text='<b>Моя вакансия:</b>\n\n' + text,
                        reply_markup=await details_vacancy_ikb(vacancy_id=vacancy_id)
                    )
                elif data.get("action") == "hide_vacancy":
                    vacancy_id = int(data.get('id'))
                    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                    vacancy.is_published = False
                    vacancy.date_created = datetime.now()
                    await CRUDVacancy.update(vacancy=vacancy)
                    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                    if vacancy.citizenship_id:
                        citizenship_id = await CRUDCitizenShip.get(citizenship_id=vacancy.citizenship_id)
                        citizenship = citizenship_id.name
                    else:
                        citizenship = "Неважно"
                    if vacancy.city_id:
                        city_id = await CRUDCity.get(city_id=vacancy.city_id)
                        city = city_id.name
                    else:
                        city = "Неважно"
                    if vacancy.work_experience_id:
                        work_experience_id = await CRUDWorkExperience.get(
                            work_experience_id=vacancy.work_experience_id)
                        work_experience = work_experience_id.name
                    else:
                        work_experience = "Неважно"
                    if vacancy.english_id:
                        english_id = await CRUDEnglish.get(english_id=vacancy.english_id)
                        english = english_id.name
                    else:
                        english = "Неважно"
                    age = await CRUDAge.get(age_id=vacancy.age_id)
                    position = await CRUDPosition.get(position_id=vacancy.position_id)
                    date_created: str = f"{str(vacancy.date_created.day)}." \
                                        f"{str(vacancy.date_created.month)}." \
                                        f"{str(vacancy.date_created.year)}"
                    visible = '<b><u>опубликована!</u></b>' \
                        if vacancy.is_published else '<b><u>не опубликована!</u></b>'

                    text = f"Ваша вакансия <i>{visible}</i>\n\n" \
                           f"Гражданство: <b>{citizenship}</b>\n" \
                           f"Город: <b>{city}</b>\n" \
                           f"Опыт работы: <b>{work_experience}</b>\n" \
                           f"Возраст: <b>{age.name}</b>\n" \
                           f"Желаемая должность: <b>{position.name}</b>\n" \
                           f"Английский: <b>{english}</b>\n" \
                           f"Дата последнего изменения: <b>{date_created}</b>"
                    await callback.answer(text="Вакансия была скрыта!")
                    await callback.message.edit_text(
                        text='<b>Моя вакансия:</b>\n\n' + text,
                        reply_markup=await details_vacancy_ikb(vacancy_id=vacancy_id)
                    )
                elif data.get("action") == "edit_vacancy":
                    vacancy_id = int(data.get('id'))
                    await callback.message.edit_text(
                        text="Редактирование вакансии:",
                        reply_markup=await edit_vacancy_ikb(vacancy_id=vacancy_id)
                    )
            # Радактирование вакансии
            elif data.get("target") == "edit_vacancy":
                if data.get("action") == "edit_citizenship":
                    vacancy_id = int(data.get('id'))
                    await EditVacancy.CitizenshipId.set()
                    await callback.message.edit_text(
                        text="Изменение гражданства:",
                        reply_markup=await list_citizenships_ikb(vacancy_id=vacancy_id)
                    )
                elif data.get("action") == "edit_city":
                    vacancy_id = int(data.get('id'))
                    await EditVacancy.CityId.set()
                    await callback.message.edit_text(
                        text="Изменение города:",
                        reply_markup=await list_cities_ikb(vacancy_id=vacancy_id)
                    )
                elif data.get("action") == "edit_work_experience":
                    vacancy_id = int(data.get('id'))
                    await EditVacancy.WorkExperienceId.set()
                    await callback.message.edit_text(
                        text="Изменение опыта работы:",
                        reply_markup=await list_work_experiences_ikb(vacancy_id=vacancy_id)
                    )
                elif data.get("action") == "edit_age":
                    vacancy_id = int(data.get('id'))
                    await EditVacancy.AgeId.set()
                    await callback.message.edit_text(
                        text="Изменение возраста:",
                        reply_markup=await list_ages_ikb(vacancy_id=vacancy_id)
                    )
                elif data.get("action") == "edit_knowledge_of_english":
                    vacancy_id = int(data.get('id'))
                    await EditVacancy.KnowledgeOfEnglish.set()
                    await callback.message.edit_text(
                        text="Изменение знания английского:",
                        reply_markup=await knowledge_of_english_ikb(vacancy_id=vacancy_id)
                    )
                elif data.get("action") == "edit_position":
                    vacancy_id = int(data.get('id'))
                    await EditVacancy.Position.set()
                    await callback.message.edit_text(
                        text="Изменение должности:",
                        reply_markup=await list_positions_ikb(vacancy_id=vacancy_id)
                    )
            # Отклики
            elif data.get("target") == "responses":
                if data.get("action") == "show":
                    my_vacancies_id = [vacancy.id for vacancy in
                                       await CRUDVacancy.get_vacancies_employer(user_id=callback.from_user.id)]
                    for vacancy_id in my_vacancies_id:
                        response = await CRUDApplicantReply.get(vacancy_id=vacancy_id)
                        if response:
                            vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                            vac_position = await CRUDPosition.get(position_id=vacancy.position_id)
                            applicant_form = await CRUDApplicantForm.get(user_id=response.user_id,
                                                                         position_id=vac_position.id)
                            position = await CRUDPosition.get(position_id=applicant_form.position_id)
                            citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form.citizenship_id)
                            work_experience = await CRUDWorkExperience.get(
                                work_experience_id=applicant_form.work_experience_id)
                            english = await CRUDEnglish.get(english_id=applicant_form.knowledge_of_english)

                            if response.status_id == 1:
                                status = "🆕 New! 🆕"
                            elif response.status_id == 2:
                                status = "❌ Отклонено! ❌"
                            elif response.status_id == 3:
                                status = "📲 На связи! 📲"
                            elif response.status_id == 4:
                                status = "✅ Одобрено! ✅"
                            else:
                                status = "‼️Статус не указан! ‼️"

                            if applicant_form.patronymic is None:
                                patronymic: str = 'N/A'
                            else:
                                patronymic = applicant_form.patronymic

                            if applicant_form.phone_number is None:
                                phone: str = 'N/A'
                            else:
                                phone = applicant_form.phone_number

                            if applicant_form.instagram_url is None:
                                insta: str = 'N/A'
                            else:
                                insta = applicant_form.instagram_url

                            date_date_of_birth: str = f"{str(applicant_form.date_of_birth.day)}." \
                                                      f"{str(applicant_form.date_of_birth.month)}." \
                                                      f"{str(applicant_form.date_of_birth.year)}"

                            recent_job_user = ' '
                            count = 1
                            get_recent_job = await CRUDRecentJob.get_name(recent_job_id=applicant_form.id)
                            if get_recent_job:
                                for i in get_recent_job:
                                    recent_job_user += f"{str(count)}.Профессия: {i.name}\n"
                                    count += 1
                            else:
                                recent_job_user = "N/A"

                            count = 0
                            text = f"Отклик №<b>{count + 1}</b>\n" \
                                   f"На позицию <b>{vac_position.name}</b>\n\n" \
                                   f"Статус заявки: <b>{status}</b>\n\n" \
                                   f"<b>Анкета:</b>\n" \
                                   f"Фамилия: <b>{applicant_form.surname}</b>\n" \
                                   f"Имя:  <b>{applicant_form.name}</b>\n" \
                                   f"Отчество:  <b>{patronymic}</b>\n" \
                                   f"Дата рождения:  <b>{date_date_of_birth}</b>\n" \
                                   f"Гражданство: <b>{citizenship.name}</b>\n" \
                                   f"Телефон:  <b>{phone}</b>\n" \
                                   f"Опыт работы:  <b>{work_experience.name}</b>\n" \
                                   f"Желаемая должность: <b>{position.name}</b>\n" \
                                   f"Английский:  <b>{english.name}</b>\n" \
                                   f"Инстаграм:  <b>{insta}</b>\n\n" \
                                   f"Последнее место работы:\n{recent_job_user}"

                            await callback.message.edit_text(text=str(text),
                                                             reply_markup=await responses_iter_ikb(
                                                                 action="page",
                                                                 target="responses",
                                                                 user_id=callback.from_user.id)
                                                             )
                            break
                        else:
                            await callback.answer(text="Откликов не найдено!")
                elif data.get("action") == "page":
                    page = int(data.get('id'))

                    my_vacancies_id = [vacancy.id for vacancy in
                                       await CRUDVacancy.get_vacancies_employer(user_id=callback.from_user.id)]
                    responses = []
                    for vacancy_id in my_vacancies_id:
                        response = await CRUDApplicantReply.get(vacancy_id=vacancy_id)
                        if response:
                            responses.append(response)

                    vacancy_id = responses[page].vacancy_id
                    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                    vac_position = await CRUDPosition.get(position_id=vacancy.position_id)
                    applicant_form = await CRUDApplicantForm.get(user_id=responses[page].user_id,
                                                                 position_id=vac_position.id)
                    position = await CRUDPosition.get(position_id=applicant_form.position_id)
                    citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form.citizenship_id)
                    work_experience = await CRUDWorkExperience.get(
                        work_experience_id=applicant_form.work_experience_id)
                    english = await CRUDEnglish.get(english_id=applicant_form.knowledge_of_english)

                    if responses[page].status_id == 1:
                        status = "🆕 New! 🆕"
                    elif responses[page].status_id == 2:
                        status = "❌ Отклонено! ❌"
                    elif responses[page].status_id == 3:
                        status = "📲 На связи! 📲"
                    elif responses[page].status_id == 4:
                        status = "✅ Одобрено! ✅"
                    else:
                        status = "‼️Статус не указан! ‼️"

                    if applicant_form.patronymic is None:
                        patronymic: str = 'N/A'
                    else:
                        patronymic = applicant_form.patronymic

                    if applicant_form.phone_number is None:
                        phone: str = 'N/A'
                    else:
                        phone = applicant_form.phone_number

                    if applicant_form.instagram_url is None:
                        insta: str = 'N/A'
                    else:
                        insta = applicant_form.instagram_url

                    date_date_of_birth: str = f"{str(applicant_form.date_of_birth.day)}." \
                                              f"{str(applicant_form.date_of_birth.month)}." \
                                              f"{str(applicant_form.date_of_birth.year)}"

                    recent_job_user = ' '
                    count = 1
                    get_recent_job = await CRUDRecentJob.get_name(recent_job_id=applicant_form.id)
                    if get_recent_job:
                        for i in get_recent_job:
                            recent_job_user += f"{str(count)}.Профессия: {i.name}\n"
                            count += 1
                    else:
                        recent_job_user = "N/A"

                    text = f"Отклик №<b>{page + 1}</b>\n" \
                           f"На позицию <b>{vac_position.name}</b>\n\n" \
                           f"Статус заявки: <b>{status}</b>\n\n" \
                           f"<b>Анкета:</b>\n" \
                           f"Фамилия: <b>{applicant_form.surname}</b>\n" \
                           f"Имя:  <b>{applicant_form.name}</b>\n" \
                           f"Отчество:  <b>{patronymic}</b>\n" \
                           f"Дата рождения:  <b>{date_date_of_birth}</b>\n" \
                           f"Гражданство: <b>{citizenship.name}</b>\n" \
                           f"Телефон:  <b>{phone}</b>\n" \
                           f"Опыт работы:  <b>{work_experience.name}</b>\n" \
                           f"Желаемая должность: <b>{position.name}</b>\n" \
                           f"Английский:  <b>{english.name}</b>\n" \
                           f"Инстаграм:  <b>{insta}</b>\n\n" \
                           f"Последнее место работы:\n{recent_job_user}"
                    await callback.message.edit_text(text=str(text),
                                                     reply_markup=await responses_iter_ikb(
                                                         action="page",
                                                         target="responses",
                                                         page=int(page),
                                                         user_id=callback.from_user.id)
                                                     )
            # Меню вакансии
            elif data.get("target") == "responses_menu":
                if data.get("action") == "show":
                    response_id = int(data.get('id'))
                    response = await CRUDApplicantReply.get(applicant_reply_id=response_id)
                    vacancy_id = response.vacancy_id
                    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                    vac_position = await CRUDPosition.get(position_id=vacancy.position_id)
                    applicant_form = await CRUDApplicantForm.get(user_id=response.user_id,
                                                                 position_id=vac_position.id)
                    position = await CRUDPosition.get(position_id=applicant_form.position_id)
                    citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form.citizenship_id)
                    work_experience = await CRUDWorkExperience.get(
                        work_experience_id=applicant_form.work_experience_id)
                    english = await CRUDEnglish.get(english_id=applicant_form.knowledge_of_english)

                    if response.status_id == 1:
                        status = "🆕 New! 🆕"
                    elif response.status_id == 2:
                        status = "❌ Отклонено! ❌"
                    elif response.status_id == 3:
                        status = "📲 На связи! 📲"
                    elif response.status_id == 4:
                        status = "✅ Одобрено! ✅"
                    else:
                        status = "‼️Статус не указан! ‼️"

                    if applicant_form.patronymic is None:
                        patronymic: str = 'N/A'
                    else:
                        patronymic = applicant_form.patronymic

                    if applicant_form.phone_number is None:
                        phone: str = 'N/A'
                    else:
                        phone = applicant_form.phone_number

                    if applicant_form.instagram_url is None:
                        insta: str = 'N/A'
                    else:
                        insta = applicant_form.instagram_url

                    date_date_of_birth: str = f"{str(applicant_form.date_of_birth.day)}." \
                                              f"{str(applicant_form.date_of_birth.month)}." \
                                              f"{str(applicant_form.date_of_birth.year)}"

                    recent_job_user = ' '
                    count = 1
                    get_recent_job = await CRUDRecentJob.get_name(recent_job_id=applicant_form.id)
                    if get_recent_job:
                        for i in get_recent_job:
                            recent_job_user += f"{str(count)}.Профессия: {i.name}\n"
                            count += 1
                    else:
                        recent_job_user = "N/A"

                    text = f"Отклик на позицию <b>{vac_position.name}</b>\n\n" \
                           f"Статус заявки: <b>{status}</b>\n\n" \
                           f"<b>Анкета:</b>\n" \
                           f"Фамилия: <b>{applicant_form.surname}</b>\n" \
                           f"Имя:  <b>{applicant_form.name}</b>\n" \
                           f"Отчество:  <b>{patronymic}</b>\n" \
                           f"Дата рождения:  <b>{date_date_of_birth}</b>\n" \
                           f"Гражданство: <b>{citizenship.name}</b>\n" \
                           f"Телефон:  <b>{phone}</b>\n" \
                           f"Опыт работы:  <b>{work_experience.name}</b>\n" \
                           f"Желаемая должность: <b>{position.name}</b>\n" \
                           f"Английский:  <b>{english.name}</b>\n" \
                           f"Инстаграм:  <b>{insta}</b>\n\n" \
                           f"Последнее место работы:\n{recent_job_user}\n\n" \
                           f"<b>Выберите действие:</b>"
                    await callback.message.edit_text(text=str(text),
                                                     reply_markup=await details_response_ikb(response_id=response_id))
                # elif data.get("action") == "contact_to_applicant":
                #     print("Hello")
                #     response_id = int(data.get('id'))
                #     response = await CRUDApplicantReply.get(applicant_reply_id=response_id)
                #     response.status_id = 3
                #     await CRUDApplicantReply.update(applicant_reply=response)
                #     response = await CRUDApplicantReply.get(applicant_reply_id=response_id)
                #     vacancy_id = response.vacancy_id
                #     vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                #     vac_position = await CRUDPosition.get(position_id=vacancy.position_id)
                #     applicant_form = await CRUDApplicantForm.get(user_id=response.user_id,
                #                                                  position_id=vac_position.id)
                #     position = await CRUDPosition.get(position_id=applicant_form.position_id)
                #     citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form.citizenship_id)
                #     work_experience = await CRUDWorkExperience.get(
                #         work_experience_id=applicant_form.work_experience_id)
                #     english = await CRUDEnglish.get(english_id=applicant_form.knowledge_of_english)
                #
                #     if response.status_id == 1:
                #         status = "🆕 New! 🆕"
                #     elif response.status_id == 2:
                #         status = "❌ Отклонено! ❌"
                #     elif response.status_id == 3:
                #         status = "📲 На связи! 📲"
                #     elif response.status_id == 4:
                #         status = "✅ Одобрено! ✅"
                #     else:
                #         status = "‼️Статус не указан! ‼️"
                #
                #     if applicant_form.patronymic is None:
                #         patronymic: str = 'N/A'
                #     else:
                #         patronymic = applicant_form.patronymic
                #
                #     if applicant_form.phone_number is None:
                #         phone: str = 'N/A'
                #     else:
                #         phone = applicant_form.phone_number
                #
                #     if applicant_form.instagram_url is None:
                #         insta: str = 'N/A'
                #     else:
                #         insta = applicant_form.instagram_url
                #
                #     date_date_of_birth: str = f"{str(applicant_form.date_of_birth.day)}." \
                #                               f"{str(applicant_form.date_of_birth.month)}." \
                #                               f"{str(applicant_form.date_of_birth.year)}"
                #
                #     recent_job_user = ' '
                #     count = 1
                #     get_recent_job = await CRUDRecentJob.get_name(recent_job_id=applicant_form.id)
                #     if get_recent_job:
                #         for i in get_recent_job:
                #             recent_job_user += f"{str(count)}.Профессия: {i.name}\n"
                #             count += 1
                #     else:
                #         recent_job_user = "N/A"
                #
                #     text = f"Отклик на позицию <b>{vac_position.name}</b>\n\n" \
                #            f"Статус заявки: <b>{status}</b>\n\n" \
                #            f"<b>Анкета:</b>\n" \
                #            f"Фамилия: <b>{applicant_form.surname}</b>\n" \
                #            f"Имя:  <b>{applicant_form.name}</b>\n" \
                #            f"Отчество:  <b>{patronymic}</b>\n" \
                #            f"Дата рождения:  <b>{date_date_of_birth}</b>\n" \
                #            f"Гражданство: <b>{citizenship.name}</b>\n" \
                #            f"Телефон:  <b>{phone}</b>\n" \
                #            f"Опыт работы:  <b>{work_experience.name}</b>\n" \
                #            f"Желаемая должность: <b>{position.name}</b>\n" \
                #            f"Английский:  <b>{english.name}</b>\n" \
                #            f"Инстаграм:  <b>{insta}</b>\n\n" \
                #            f"Последнее место работы:\n{recent_job_user}\n\n" \
                #            f"<b>Выберите действие:</b>"
                #     await callback.message.edit_text(text=str(text),
                #                                      reply_markup=await details_response_ikb(response_id=response_id))
                elif data.get("action") == "approve_response":
                    response_id = int(data.get('id'))
                    response = await CRUDApplicantReply.get(applicant_reply_id=response_id)
                    response.status_id = 4
                    await CRUDApplicantReply.update(applicant_reply=response)
                    await callback.answer(text="Отклик одобрен!")
                    response = await CRUDApplicantReply.get(applicant_reply_id=response_id)
                    vacancy_id = response.vacancy_id
                    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                    vac_position = await CRUDPosition.get(position_id=vacancy.position_id)
                    applicant_form = await CRUDApplicantForm.get(user_id=response.user_id,
                                                                 position_id=vac_position.id)
                    position = await CRUDPosition.get(position_id=applicant_form.position_id)
                    citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form.citizenship_id)
                    work_experience = await CRUDWorkExperience.get(
                        work_experience_id=applicant_form.work_experience_id)
                    english = await CRUDEnglish.get(english_id=applicant_form.knowledge_of_english)

                    if response.status_id == 1:
                        status = "🆕 New! 🆕"
                    elif response.status_id == 2:
                        status = "❌ Отклонено! ❌"
                    elif response.status_id == 3:
                        status = "📲 На связи! 📲"
                    elif response.status_id == 4:
                        status = "✅ Одобрено! ✅"
                    else:
                        status = "‼️Статус не указан! ‼️"

                    if applicant_form.patronymic is None:
                        patronymic: str = 'N/A'
                    else:
                        patronymic = applicant_form.patronymic

                    if applicant_form.phone_number is None:
                        phone: str = 'N/A'
                    else:
                        phone = applicant_form.phone_number

                    if applicant_form.instagram_url is None:
                        insta: str = 'N/A'
                    else:
                        insta = applicant_form.instagram_url

                    date_date_of_birth: str = f"{str(applicant_form.date_of_birth.day)}." \
                                              f"{str(applicant_form.date_of_birth.month)}." \
                                              f"{str(applicant_form.date_of_birth.year)}"

                    recent_job_user = ' '
                    count = 1
                    get_recent_job = await CRUDRecentJob.get_name(recent_job_id=applicant_form.id)
                    if get_recent_job:
                        for i in get_recent_job:
                            recent_job_user += f"{str(count)}.Профессия: {i.name}\n"
                            count += 1
                    else:
                        recent_job_user = "N/A"

                    text = f"Отклик на позицию <b>{vac_position.name}</b>\n\n" \
                           f"Статус заявки: <b>{status}</b>\n\n" \
                           f"<b>Анкета:</b>\n" \
                           f"Фамилия: <b>{applicant_form.surname}</b>\n" \
                           f"Имя:  <b>{applicant_form.name}</b>\n" \
                           f"Отчество:  <b>{patronymic}</b>\n" \
                           f"Дата рождения:  <b>{date_date_of_birth}</b>\n" \
                           f"Гражданство: <b>{citizenship.name}</b>\n" \
                           f"Телефон:  <b>{phone}</b>\n" \
                           f"Опыт работы:  <b>{work_experience.name}</b>\n" \
                           f"Желаемая должность: <b>{position.name}</b>\n" \
                           f"Английский:  <b>{english.name}</b>\n" \
                           f"Инстаграм:  <b>{insta}</b>\n\n" \
                           f"Последнее место работы:\n{recent_job_user}\n\n" \
                           f"<b>Выберите действие:</b>"
                    await callback.message.edit_text(text=str(text),
                                                     reply_markup=await details_response_ikb(response_id=response_id))
                elif data.get("action") == "reject_response":
                    response_id = int(data.get('id'))
                    response = await CRUDApplicantReply.get(applicant_reply_id=response_id)
                    response.status_id = 2
                    await CRUDApplicantReply.update(applicant_reply=response)
                    await callback.answer(text="Отклик отклонен!")
                    response = await CRUDApplicantReply.get(applicant_reply_id=response_id)
                    vacancy_id = response.vacancy_id
                    vacancy = await CRUDVacancy.get(vacancy_id=vacancy_id)
                    vac_position = await CRUDPosition.get(position_id=vacancy.position_id)
                    applicant_form = await CRUDApplicantForm.get(user_id=response.user_id,
                                                                 position_id=vac_position.id)
                    position = await CRUDPosition.get(position_id=applicant_form.position_id)
                    citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form.citizenship_id)
                    work_experience = await CRUDWorkExperience.get(
                        work_experience_id=applicant_form.work_experience_id)
                    english = await CRUDEnglish.get(english_id=applicant_form.knowledge_of_english)

                    if response.status_id == 1:
                        status = "🆕 New! 🆕"
                    elif response.status_id == 2:
                        status = "❌ Отклонено! ❌"
                    elif response.status_id == 3:
                        status = "📲 На связи! 📲"
                    elif response.status_id == 4:
                        status = "✅ Одобрено! ✅"
                    else:
                        status = "‼️Статус не указан! ‼️"

                    if applicant_form.patronymic is None:
                        patronymic: str = 'N/A'
                    else:
                        patronymic = applicant_form.patronymic

                    if applicant_form.phone_number is None:
                        phone: str = 'N/A'
                    else:
                        phone = applicant_form.phone_number

                    if applicant_form.instagram_url is None:
                        insta: str = 'N/A'
                    else:
                        insta = applicant_form.instagram_url

                    date_date_of_birth: str = f"{str(applicant_form.date_of_birth.day)}." \
                                              f"{str(applicant_form.date_of_birth.month)}." \
                                              f"{str(applicant_form.date_of_birth.year)}"

                    recent_job_user = ' '
                    count = 1
                    get_recent_job = await CRUDRecentJob.get_name(recent_job_id=applicant_form.id)
                    if get_recent_job:
                        for i in get_recent_job:
                            recent_job_user += f"{str(count)}.Профессия: {i.name}\n"
                            count += 1
                    else:
                        recent_job_user = "N/A"

                    text = f"Отклик на позицию <b>{vac_position.name}</b>\n\n" \
                           f"Статус заявки: <b>{status}</b>\n\n" \
                           f"<b>Анкета:</b>\n" \
                           f"Фамилия: <b>{applicant_form.surname}</b>\n" \
                           f"Имя:  <b>{applicant_form.name}</b>\n" \
                           f"Отчество:  <b>{patronymic}</b>\n" \
                           f"Дата рождения:  <b>{date_date_of_birth}</b>\n" \
                           f"Гражданство: <b>{citizenship.name}</b>\n" \
                           f"Телефон:  <b>{phone}</b>\n" \
                           f"Опыт работы:  <b>{work_experience.name}</b>\n" \
                           f"Желаемая должность: <b>{position.name}</b>\n" \
                           f"Английский:  <b>{english.name}</b>\n" \
                           f"Инстаграм:  <b>{insta}</b>\n\n" \
                           f"Последнее место работы:\n{recent_job_user}\n\n" \
                           f"<b>Выберите действие:</b>"
                    await callback.message.edit_text(text=str(text),
                                                     reply_markup=await details_response_ikb(response_id=response_id))
            # Кандидаты
            elif data.get("target") == "candidates":
                if data.get("action") == "show":
                    vacancy_id = int(data.get('id'))
                    candidates: list = []
                    for i in await CRUDApplicantForm.get_all(is_published=True):
                        if await CRUDVacancy.get(vacancy_id=vacancy_id, position_id=i.position_id):
                            if await CRUDEmployerReply.get_candidate_for_vacancy(vacancy_id=vacancy_id,
                                                                                 candidate_id=i.user_id
                                                                                 ) is None:
                                candidates.append(i)

                    if candidates:
                        citizenship = await CRUDCitizenShip.get(citizenship_id=candidates[0].citizenship_id)
                        position = await CRUDPosition.get(position_id=candidates[0].position_id)
                        work_experience = await CRUDWorkExperience.get(
                            work_experience_id=candidates[0].work_experience_id)
                        english = await CRUDEnglish.get(english_id=candidates[0].knowledge_of_english)

                        if candidates[0].patronymic is None:
                            patronymic: str = 'N/A'
                        else:
                            patronymic = candidates[0].patronymic

                        if candidates[0].phone_number is None:
                            phone: str = 'N/A'
                        else:
                            phone = candidates[0].phone_number

                        if candidates[0].instagram_url is None:
                            insta: str = 'N/A'
                        else:
                            insta = candidates[0].instagram_url

                        date_date_of_birth: str = f"{str(candidates[0].date_of_birth.day)}." \
                                                  f"{str(candidates[0].date_of_birth.month)}." \
                                                  f"{str(candidates[0].date_of_birth.year)}"

                        recent_job_user = ' '
                        count = 1
                        get_recent_job = await CRUDRecentJob.get_name(recent_job_id=candidates[0].id)
                        if get_recent_job:
                            for i in get_recent_job:
                                recent_job_user += f"{str(count)}.Профессия: {i.name}\n"
                                count += 1
                        else:
                            recent_job_user = "N/A"

                        count_candidate = 0
                        text = f"<b>Для данной вакансии доступно кандидатов:</b> {len(candidates)}\n" \
                               f"Кандидат №{count_candidate + 1}\n\n" \
                               f"Фамилия: <b>{candidates[0].surname}</b>\n" \
                               f"Имя:  <b>{candidates[0].name}</b>\n" \
                               f"Отчество:  <b>{patronymic}</b>\n" \
                               f"Дата рождения:  <b>{date_date_of_birth}</b>\n" \
                               f"Гражданство: <b>{citizenship.name}</b>\n" \
                               f"Телефон:  <b>{phone}</b>\n" \
                               f"Опыт работы:  <b>{work_experience.name}</b>\n" \
                               f"Желаемая должность: <b>{position.name}</b>\n" \
                               f"Английский:  <b>{english.name}</b>\n" \
                               f"Инстаграм:  <b>{insta}</b>\n\n" \
                               f"Последнее место работы:\n{recent_job_user}\n\n"
                        await callback.message.edit_text(text=str(text),
                                                         reply_markup=await candidates_iter_ikb(
                                                             action="page",
                                                             target="candidates",
                                                             vacancy_id=vacancy_id)
                                                         )
                    else:
                        await callback.answer("Подходящих кандидатов нет!")
                elif data.get("action") == "page":
                    page = int(data.get("id").split('_')[0])
                    vacancy_id = int(data.get("id").split('_')[1])
                    candidates: list = []
                    for i in await CRUDApplicantForm.get_all(is_published=True):
                        if await CRUDVacancy.get(vacancy_id=vacancy_id, position_id=i.position_id):
                            if await CRUDEmployerReply.get_candidate_for_vacancy(vacancy_id=vacancy_id,
                                                                                 candidate_id=i.user_id
                                                                                 ) is None:
                                candidates.append(i)

                    if candidates:
                        citizenship = await CRUDCitizenShip.get(citizenship_id=candidates[page].citizenship_id)
                        position = await CRUDPosition.get(position_id=candidates[page].position_id)
                        work_experience = await CRUDWorkExperience.get(
                            work_experience_id=candidates[page].work_experience_id)
                        english = await CRUDEnglish.get(english_id=candidates[page].knowledge_of_english)

                        if candidates[page].patronymic is None:
                            patronymic: str = 'N/A'
                        else:
                            patronymic = candidates[page].patronymic

                        if candidates[page].phone_number is None:
                            phone: str = 'N/A'
                        else:
                            phone = candidates[page].phone_number

                        if candidates[page].instagram_url is None:
                            insta: str = 'N/A'
                        else:
                            insta = candidates[page].instagram_url

                        date_date_of_birth: str = f"{str(candidates[page].date_of_birth.day)}." \
                                                  f"{str(candidates[page].date_of_birth.month)}." \
                                                  f"{str(candidates[page].date_of_birth.year)}"

                        recent_job_user = ' '
                        count = 1
                        get_recent_job = await CRUDRecentJob.get_name(recent_job_id=candidates[page].id)
                        if get_recent_job:
                            for i in get_recent_job:
                                recent_job_user += f"{str(count)}.Профессия: {i.name}\n"
                                count += 1
                        else:
                            recent_job_user = "N/A"

                        text = f"<b>Для данной вакансии доступно кандидатов:</b> {len(candidates)}\n" \
                               f"Кандидат №{page + 1}\n\n" \
                               f"Фамилия: <b>{candidates[page].surname}</b>\n" \
                               f"Имя:  <b>{candidates[page].name}</b>\n" \
                               f"Отчество:  <b>{patronymic}</b>\n" \
                               f"Дата рождения:  <b>{date_date_of_birth}</b>\n" \
                               f"Гражданство: <b>{citizenship.name}</b>\n" \
                               f"Телефон:  <b>{phone}</b>\n" \
                               f"Опыт работы:  <b>{work_experience.name}</b>\n" \
                               f"Желаемая должность: <b>{position.name}</b>\n" \
                               f"Английский:  <b>{english.name}</b>\n" \
                               f"Инстаграм:  <b>{insta}</b>\n\n" \
                               f"Последнее место работы:\n{recent_job_user}\n\n"
                        await callback.message.edit_text(text=str(text),
                                                         reply_markup=await candidates_iter_ikb(
                                                             action="page",
                                                             target="candidates",
                                                             page=int(page),
                                                             vacancy_id=vacancy_id)
                                                         )
                elif data.get("action") == "invite":
                    candidate_id = int(data.get("id").split('_')[0])
                    vacancy_id = int(data.get("id").split('_')[1])
                    await state.update_data(candidate_id=candidate_id)
                    await state.update_data(vacancy_id=vacancy_id)
                    await InviteCandidate.Text.set()
                    await callback.message.edit_text(
                        text="<b>Введите сопроводительный текст (в формате HTML разметки)</b>:"
                    )
            # Поддержка
            elif data.get("target") == "support":
                if data.get("action") == "show":
                    text = f"\n\n" \
                           f"📱 <b>Контактный номер телефона:</b> {CONFIG.SUPPORT.PHONE}\n\n" \
                           f"📧 <b>Email:</b> {CONFIG.SUPPORT.EMAIL}\n\n" \
                           f"📷 <b>Instagram:</b> <a href='www.instagram.com/{CONFIG.SUPPORT.INSTAGRAM}/" \
                           f"'>{CONFIG.SUPPORT.INSTAGRAM}</a>\n\n" \
                           f"🎧 <b>Discord:</b> <code>{CONFIG.SUPPORT.DISCORD}</code>\n\n"
                    await callback.message.edit_text(text=f"<b>Способ связи:</b> {text}",
                                                     reply_markup=await back_in_main_menu_ikb(),
                                                     parse_mode="HTML")
            # Кнопка назад
            elif data.get("target") == "back":
                if data.get("action") == "cancel":
                    await state.finish()
                    await callback.message.edit_text(
                        text="Меню работодателя",
                        reply_markup=await employer_ikb()
                    )
                elif data.get("action") == "back_citizenships":
                    await AddVacancy.CitizenshipId.set()
                    await callback.message.edit_text(
                        text="Выберите гражданство, которое должно быть у соискателя:",
                        reply_markup=await list_citizenships_ikb()
                    )
                elif data.get("action") == "back_cities":
                    await AddVacancy.CityId.set()
                    await callback.message.edit_text(
                        text="Выберите город, который должен быть у соискателя:",
                        reply_markup=await list_cities_ikb()
                    )
                elif data.get("action") == "back_work_experiences":
                    await AddVacancy.WorkExperienceId.set()
                    await callback.message.edit_text(
                        text="Выберите опыт работы, который должен быть у соискателя:",
                        reply_markup=await list_work_experiences_ikb()
                    )
                elif data.get("action") == "back_ages":
                    await AddVacancy.AgeId.set()
                    await callback.message.edit_text(
                        text="Выберите желаемый возраст соискателя:",
                        reply_markup=await list_ages_ikb()
                    )
                elif data.get("action") == "back_english":
                    await AddVacancy.KnowledgeOfEnglish.set()
                    await callback.message.edit_text(
                        text="У соискателя должно быть знание английского?:",
                        reply_markup=await knowledge_of_english_ikb()
                    )
                elif data.get("action") == "back_positions":
                    state_data: dict = await state.get_data()
                    subpositions = list(state_data["subpositions"])
                    await AddVacancy.Position.set()
                    await callback.message.edit_text(
                        text="Выберите должность:",
                        reply_markup=await list_positions_ikb(subpositions_id=subpositions)
                    )
                elif data.get("action") == "back_subpositions":
                    position_id = int(data.get("id"))
                    position = await CRUDPosition.get(position_id=position_id)
                    state_data: dict = await state.get_data()
                    subpositions = list(state_data["subpositions"])
                    await AddVacancy.SubPosition.set()
                    await callback.message.edit_text(
                        text=f"Выберите специальность для должности {position.name}:",
                        reply_markup=await list_subpositions_ikb(position_id=position_id,
                                                                 subpositions_id=subpositions)
                    )
        elif message:
            await message.delete()
            try:
                await bot.delete_message(
                    chat_id=message.from_user.id,
                    message_id=message.message_id - 1
                )
            except BadRequest:
                pass
            if state:
                # Приглашение кандидата
                if await state.get_state() == "InviteCandidate:Text":
                    await state.update_data(text=message.text)
                    await InviteCandidate.Approve.set()
                    await message.answer(
                        text=f"<b>Проверьте правильность введенных данных:</b>\n"
                             f"{message.text}",
                        reply_markup=await approve_invite_candidate(),
                        parse_mode="HTML"
                    )
