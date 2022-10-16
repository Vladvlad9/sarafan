import re
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest
from crud import CRUDApplicantForm, CRUDCitizenShip, CRUDCity, CRUDWorkExperience, CRUDPosition, CRUDRecentJob
from crud.applicant_reply import CRUDApplicantReply
from crud.english import CRUDEnglish
from crud.users import CRUDUser
from crud.vacancy import CRUDVacancy
from enums import Roles, Statuses
from keyboards.inline.users.employer import employer_cb
from loader import bot
from schemas import UserSchema, RecentJobSchema, ApplicantReplySchema
from states.users import EditProfile
from keyboards.inline.users.сalendar import DialogCalendar, calendar_callback

from config import CONFIG
from utils.telegraph_library import TelegraphPage

register_cb = CallbackData("reg", "target", "id", "editId")
profile_cb = CallbackData("profile", "target", "id", "editId")


class Profile:
    @staticmethod
    async def back(user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="← Назад",
                                         callback_data=profile_cb.new("editQuestionnaire", 0,
                                                                      user_id))
                ]
            ]
        )

    @staticmethod
    async def back_registration(user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data=profile_cb.new("editQuestionnaire", 0,
                                                                      user_id))
                ]
            ]
        )

    @staticmethod
    async def support_ikb() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="← Назад", callback_data=profile_cb.new("looking_work", 0, 0))]
            ]
        )

    @staticmethod
    async def recent_job_ikb(recent_job_id: int, user_id: int) -> InlineKeyboardMarkup:
        recent_job = await CRUDRecentJob.get_name(recent_job_id=recent_job_id)

        keyboards = [
            [
                InlineKeyboardButton(
                    text=f"{recent_jobs.name} ✏",
                    callback_data=profile_cb.new("recentJobEdit", recent_jobs.id, user_id)
                ),
                InlineKeyboardButton(
                    text="❌",
                    callback_data=profile_cb.new("DelrecentJob", recent_jobs.id, user_id)
                )

            ]
            for recent_jobs in recent_job
        ]
        if len(recent_job) == 3:
            keyboards.append(
                [InlineKeyboardButton(text="← Назад", callback_data=profile_cb.new("editQuestionnaire", 0, user_id))]),
        else:
            if len(recent_job) >= 1:
                keyboards.append(
                    [InlineKeyboardButton(text="➕", callback_data=profile_cb.new("addRecentJob", 1, user_id))] +
                    [InlineKeyboardButton(text="← Назад",
                                          callback_data=profile_cb.new("editQuestionnaire", 0, user_id))]
                )
            else:
                keyboards.append(
                    [
                        InlineKeyboardButton(text="➕", callback_data=profile_cb.new("addRecentJob", 2, user_id)),
                        InlineKeyboardButton(text="← Назад",
                                             callback_data=profile_cb.new("editQuestionnaire", 4, user_id)),
                    ]
                )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=keyboards
        )
        return keyboard

    @staticmethod
    async def send_contact_ikb(user_id: int) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            row_width=2,
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text='Поделиться контактом',
                                   request_contact=True),
                    KeyboardButton(text='Назад', callback_data=profile_cb.new("editQuestionnaire", 0, user_id))
                ]
            ]
        )

    @staticmethod
    async def citizenship_ikb(user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text=cityzenShip.name,
                                                         callback_data=profile_cb.new("CitizenshipEdit", cityzenShip.id,
                                                                                      user_id))
                                ]
                                for cityzenShip in await CRUDCitizenShip.get_all()
                            ] + [
                                [
                                    InlineKeyboardButton(text="← Назад",
                                                         callback_data=profile_cb.new("editQuestionnaire", 0, user_id))
                                ]
                            ]
        )

    @staticmethod
    async def english_ikb(user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text=english.name,
                                                         callback_data=profile_cb.new("EnglishEdit", english.id,
                                                                                      user_id))
                                ]
                                for english in await CRUDEnglish.get_all()
                            ] + [
                                [
                                    InlineKeyboardButton(text="← Назад",
                                                         callback_data=profile_cb.new("editQuestionnaire", 0, user_id))
                                ]
                            ]
        )

    @staticmethod
    async def work_experience_ikb(user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text=work_experience.name,
                                                         callback_data=profile_cb.new("WorkExperienceEdit",
                                                                                      work_experience.id, user_id)
                                                         )
                                ]
                                for work_experience in await CRUDWorkExperience.get_all()
                            ] + [
                                [
                                    InlineKeyboardButton(text="←Назад",
                                                         callback_data=profile_cb.new("editQuestionnaire", 0, user_id))
                                ]
                            ]
        )

    @staticmethod
    async def subpositions_ikb(position_id: int, user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=subpositions.name,
                                         callback_data=profile_cb.new("RecentJob", subpositions.id, user_id)
                                         )
                ]
                for subpositions in await CRUDPosition.get_all_subpositions(position_id=position_id)
            ]
        )

    @staticmethod
    async def position_ikb(user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text=position.name,
                                                         callback_data=profile_cb.new("SubpositionsEdit",
                                                                                      position.id, user_id))
                                ]
                                for position in await CRUDPosition.get_all_positions()
                            ] + [
                                [
                                    InlineKeyboardButton(text="← Назад",
                                                         callback_data=profile_cb.new("editQuestionnaire", 0, user_id))
                                ]
                            ]
        )

    @staticmethod
    async def approve_ikb(target: str, user_id: int, scheduler: bool = None) -> InlineKeyboardMarkup:
        if scheduler:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Да", callback_data=profile_cb.new(target, 1, user_id)),
                        InlineKeyboardButton(text="Нет", callback_data=profile_cb.new(target, 0, user_id))
                    ]
                ]
            )
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Да", callback_data=profile_cb.new(target, 1, user_id)),
                        InlineKeyboardButton(text="Нет", callback_data=profile_cb.new(target, 0, user_id))
                    ],
                    [
                        InlineKeyboardButton(text="← Назад",
                                             callback_data=profile_cb.new("editQuestionnaire", 3, user_id))
                    ]
                ]
            )
        return keyboard

    @staticmethod
    async def cities_ikb(user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=city.name,
                        callback_data=profile_cb.new("cityEdit", city.id, user_id)
                    )
                    for city in await CRUDCity.get_all()
                ],
                [
                    InlineKeyboardButton(
                        text="← Назад",
                        callback_data=profile_cb.new("editQuestionnaire", 0, user_id)
                    )
                ]
            ]
        )

    @staticmethod
    async def looking_ikb() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Ищу работу",
                                         callback_data=register_cb.new("date_of_birth", 0, 0)),
                    InlineKeyboardButton(text="Ищу сотрудников",
                                         callback_data=employer_cb.new("show_menu", "employer", 0))
                ]
            ]
        )
        return keyboard

    @staticmethod
    async def profile_ikb(user_id: int) -> InlineKeyboardMarkup:
        vacancies = await CRUDApplicantForm.get(user_id=user_id)
        if vacancies:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Заполнить анкету",
                                          callback_data=register_cb.new("date_of_birth", 0, 0))],
                    [InlineKeyboardButton(text="Мои анкеты",
                                          callback_data=profile_cb.new("my_questionnaires", 1, user_id))],
                    [InlineKeyboardButton(text="Мои отклики", callback_data=profile_cb.new("responses", 1, user_id))],
                    [InlineKeyboardButton(text="Вакансии", callback_data=profile_cb.new("vacancies", 1, user_id))],
                    [InlineKeyboardButton(text="Поддержка", callback_data=profile_cb.new("support", 1, user_id))]
                ]
            )
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Заполнить анкету",
                                          callback_data=register_cb.new("date_of_birth", 0, 0))],
                    [InlineKeyboardButton(text="Мои анкеты",
                                          callback_data=profile_cb.new("my_questionnaires", 1, user_id))],
                    [InlineKeyboardButton(text="Мои отклики", callback_data=profile_cb.new("responses", 1, user_id))],
                    [InlineKeyboardButton(text="Поддержка", callback_data=profile_cb.new("support", 1, user_id))]
                ]
            )
        return keyboard

    @staticmethod
    async def edit_ikb(current_user: int = 0) -> InlineKeyboardMarkup:
        user = await CRUDApplicantForm.get(applicant_form_id=current_user)
        if user.is_published:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Удалить",
                                          callback_data=profile_cb.new("deleteQuestionnaire", user.id, current_user))],
                    [InlineKeyboardButton(text="Редактировать",
                                          callback_data=profile_cb.new("editQuestionnaire", 0, current_user))],
                    [InlineKeyboardButton(text="Скрыть",
                                          callback_data=profile_cb.new("hideQuestionnaire", 2, current_user))],
                    [InlineKeyboardButton(text="← Назад",
                                          callback_data=profile_cb.new("my_questionnaires", 3, current_user))]
                ]
            )
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Удалить",
                                          callback_data=profile_cb.new("deleteQuestionnaire", 0, current_user))],
                    [InlineKeyboardButton(text="Редактировать",
                                          callback_data=profile_cb.new("editQuestionnaire", 0, current_user))],

                    [InlineKeyboardButton(text="Опубликовать",
                                          callback_data=profile_cb.new("publishQuestionnaire", 2, current_user))],
                    [InlineKeyboardButton(text="← Назад",
                                          callback_data=profile_cb.new("my_questionnaires", 3, current_user))]
                ]
            )
        return keyboard

    @staticmethod
    async def orders_iter_ikb(target: str,
                              user_id: int,
                              vacancies: list = None,
                              responses: bool = None,
                              page: int = 0) -> InlineKeyboardMarkup:
        if vacancies:
            orders = vacancies
        elif responses:
            orders = await CRUDApplicantReply.get_all(user_id=user_id)
        else:
            orders = await CRUDApplicantForm.get_all(user_id=user_id)

        orders_count = len(orders)

        prev_page: int
        next_page: int

        if page == 0:
            prev_page = orders_count - 1
            next_page = page + 1
        elif page == orders_count - 1:
            prev_page = page - 1
            next_page = 0
        else:
            prev_page = page - 1
            next_page = page + 1

        back_ikb = InlineKeyboardButton("Назад", callback_data=profile_cb.new("looking_work", 0, 0))
        prev_page_ikb = InlineKeyboardButton("←", callback_data=profile_cb.new(target, prev_page, 0))
        next_page_ikb = InlineKeyboardButton("→", callback_data=profile_cb.new(target, next_page, 0))

        if vacancies:
            response_ikb = InlineKeyboardButton(text="Откликнуться",
                                                callback_data=profile_cb.new("response_vacancies", vacancies[page].id,
                                                                             0))
            if orders_count == 1:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            response_ikb,
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
                        ],
                        [
                            response_ikb, back_ikb]
                    ]
                )
        elif responses:
            if orders_count == 1:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
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
                        ],
                        [
                            back_ikb]
                    ]
                )
        else:
            orders_ikb = InlineKeyboardButton("☰", callback_data=profile_cb.new("orderMenu", orders[page].id, 0))
            if orders_count == 1:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            orders_ikb,
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
                            orders_ikb,
                        ],
                        [back_ikb]
                    ]
                )

    @staticmethod
    async def editQuestionnaire_ikb(current_user: int = None) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"Фамилия", callback_data=profile_cb.new("Edit", 0, current_user))
                ],
                [
                    InlineKeyboardButton(text="Имя", callback_data=profile_cb.new("Edit", 1, current_user)),
                ],
                [
                    InlineKeyboardButton(text=f"Отчество", callback_data=profile_cb.new("Edit", 2, current_user)),
                ],
                [
                    InlineKeyboardButton(text=f"Дата рождения", callback_data=profile_cb.new("Edit", 3, current_user))
                ],
                [
                    InlineKeyboardButton(text=f"Гражданство", callback_data=profile_cb.new("Edit", 4, current_user))
                ],
                [
                    InlineKeyboardButton(text=f"Телефон", callback_data=profile_cb.new("Edit", 5, current_user))
                ],
                # [
                #     InlineKeyboardButton(text=f"Город", callback_data=profile_cb.new("Edit", 6, current_user))
                # ],
                # [
                #     InlineKeyboardButton(text=f"Семейное положение",
                #                          callback_data=profile_cb.new("Edit", 7, current_user))
                # ],
                [
                    InlineKeyboardButton(text=f"Инстаграм", callback_data=profile_cb.new("Edit", 8, current_user))
                ],
                [
                    InlineKeyboardButton(text=f"Английский", callback_data=profile_cb.new("Edit", 9, current_user))
                ],
                [
                    InlineKeyboardButton(text=f"Стаж", callback_data=profile_cb.new("Edit", 10, current_user))
                ],
                [
                    InlineKeyboardButton(text=f"Желаемое место работы",
                                         callback_data=profile_cb.new("Edit", 11, current_user))
                ],
                [
                    InlineKeyboardButton(text=f"Последние места работы",
                                         callback_data=profile_cb.new("Edit", 12, current_user))
                ],

                [InlineKeyboardButton(text="← Назад",
                                      callback_data=profile_cb.new("orderMenu", current_user, current_user))],
            ]
        )
        return keyboard

    @staticmethod
    async def process_profile(callback: CallbackQuery = None, message: Message = None,
                              state: FSMContext = None) -> None:
        if callback:
            if callback.data.startswith('profile'):
                data = profile_cb.parse(callback_data=callback.data)
                # Меню Пользователя который ищет работу
                if data.get("target") == "looking_work":
                    # await Profile.on_startup(user_id=callback.from_user.id)
                    await callback.message.edit_text(text='Профиль',
                                                     reply_markup=await Profile.profile_ikb(callback.from_user.id))

                # Меню Пользователя который ищет сотрудников
                if data.get("target") == "looking_employee":
                    await CRUDUser.add(user=UserSchema(id=callback.from_user.id, role_id=Roles.Employer.value))
                    await callback.message.edit_text('Гланое меню')

                # Мои Анкеты
                if data.get("target") == "my_questionnaires":
                    applicant_form = await CRUDApplicantForm.get(user_id=callback.from_user.id)

                    if applicant_form:
                        citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form.citizenship_id)
                        work_experience = await CRUDWorkExperience.get(
                            work_experience_id=applicant_form.work_experience_id)
                        position = await CRUDPosition.get(position_id=applicant_form.position_id)
                        knowledge_of_english = await CRUDEnglish.get(english_id=applicant_form.knowledge_of_english)


                        patronymic = ""
                        insta = ""
                        phone = ""
                        if applicant_form.patronymic is None:
                            patronymic: str = 'N/A'
                        else:
                            patronymic = applicant_form.patronymic

                        if applicant_form.phone_number is None:
                            phone: str = 'N/A'
                        else:
                            phone: str = applicant_form.phone_number

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

                        visible = ""
                        if applicant_form.is_published:
                            visible = ' <b><u>видит</u></b> роботадатель'
                        else:
                            visible = ' <b><u>не видит</u></b> работадатель'

                        text = f"<i>Вашу анкету {visible}</i>\n\n" \
                               f"<b>Фамилия</b>: {applicant_form.surname}\n" \
                               f"<b>Имя:</b>  {applicant_form.name}\n" \
                               f"<b>Отчество:</b>  {patronymic}\n" \
                               f"<b>Дата рождения:</b>  {date_date_of_birth}\n" \
                               f"<b>Гражданство:</b> {citizenship.name}\n" \
                               f"<b>Телефон:</b>  {phone}\n" \
                               f"<b>Опыт работы:</b>  {work_experience.name}\n" \
                               f"<b>Желаемая должность:</b> {position.name}\n" \
                               f"<b>Английский:</b>  {knowledge_of_english.name}\n" \
                               f"<b>Инстаграм</b>: <a href='https://www.instagram.com/{insta}/'>{insta}</a>\n\n" \
                               f"<b>Последнее место работы:</b>\n{recent_job_user}"

                        await callback.message.edit_text(f'Мои анкеты\n{text}',
                                                         reply_markup=await Profile.orders_iter_ikb(
                                                             target="page", user_id=callback.from_user.id),
                                                         parse_mode="HTML"
                                                         )
                    else:
                        await callback.answer("Анкет нет")

                # # Добавить анкету
                # if data.get("target") == "add_questionnaires":
                #     await callback.message.edit_text("Заполните анкету", reply_markup=InlineKeyboardMarkup(
                #         inline_keyboard=[
                #             [
                #                 InlineKeyboardButton(
                #                     text="Заполнить анкету",
                #                     callback_data=register_cb.new("date_of_birth", 0, 0)
                #                 )
                #             ]
                #         ]
                #     ))
                #
                # # Пагинация для анкет
                if data.get("target") == "page":
                    page = int(data.get('id'))

                    applicant_form = await CRUDApplicantForm.get_all(user_id=callback.from_user.id)

                    citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form[page].citizenship_id)
                    work_experience = await CRUDWorkExperience.get(
                        work_experience_id=applicant_form[page].work_experience_id)
                    position = await CRUDPosition.get(position_id=applicant_form[page].position_id)
                    knowledge_of_english = await CRUDEnglish.get(english_id=applicant_form[page].knowledge_of_english)

                    patronymic = ""
                    insta = ""
                    phone = ""
                    if applicant_form[page].patronymic is None:
                        patronymic: str = 'N/A'
                    else:
                        patronymic = applicant_form[page].patronymic

                    if applicant_form[page].phone_number is None:
                        phone: str = 'N/A'
                    else:
                        phone = applicant_form[page].phone_number

                    if applicant_form[page].instagram_url is None:
                        insta: str = 'N/A'
                    else:
                        insta = applicant_form[page].instagram_url

                    date_date_of_birth: str = f"{str(applicant_form[page].date_of_birth.day)}." \
                                              f"{str(applicant_form[page].date_of_birth.month)}." \
                                              f"{str(applicant_form[page].date_of_birth.year)}"

                    recent_job_user = ' '
                    count = 1
                    get_recent_job = await CRUDRecentJob.get_name(recent_job_id=applicant_form[page].id)
                    if get_recent_job:
                        for i in get_recent_job:
                            recent_job_user += f"{str(count)}.Профессия: {i.name}\n"
                            count += 1
                    else:
                        recent_job_user = "N/A"

                    visible = ""
                    if applicant_form[page].is_published:
                        visible = ' <b><u>видит</u></b> роботадатель'
                    else:
                        visible = ' <b><u>не видит</u></b> работадатель'

                    text = f"<i>Вашу анкету {visible}</i>\n\n" \
                           f"<b>Фамилия</b>: {applicant_form[page].surname}\n" \
                           f"<b>Имя:</b>  {applicant_form[page].name}\n" \
                           f"<b>Отчество:</b>  {patronymic}\n" \
                           f"<b>Дата рождения:</b>  {date_date_of_birth}\n" \
                           f"<b>Гражданство:</b> {citizenship.name}\n" \
                           f"<b>Телефон:</b>  {phone}\n" \
                           f"<b>Опыт работы:</b>  {work_experience.name}\n" \
                           f"<b>Желаемая должность:</b> {position.name}\n" \
                           f"<b>Английский:</b>  {knowledge_of_english.name}\n" \
                           f"<b>Инстаграм</b>: <a href='https://www.instagram.com/{insta}/'>{insta}</a>\n\n" \
                           f"<b>Последнее место работы:</b>\n{recent_job_user}"
                    await callback.message.edit_text(
                        'Мои анкеты\n' + text,
                        reply_markup=await Profile.orders_iter_ikb(target="page",
                                                                   page=int(page),
                                                                   user_id=callback.from_user.id
                                                                   ), parse_mode="HTML"
                    )

                # Пагинация для Вакансий
                if data.get("target") == "page_vacancies":
                    page = int(data.get('id'))

                    applicant_replies_id: list = list(
                        map(lambda x: x.vacancy_id, await CRUDApplicantReply.get_all(user_id=callback.from_user.id))
                    )

                    vacancies: list = await CRUDVacancy.get_all(is_published=True)
                    vacancies = list(filter(lambda x: x.id not in applicant_replies_id, vacancies))

                    get_vacancies: list = []
                    applicant_forms: list = await CRUDApplicantForm.get_all(user_id=callback.from_user.id)
                    for vacancy in vacancies:
                        for applicant_form in applicant_forms:
                            if vacancy.position_id == applicant_form.position_id:
                                get_vacancies.append(vacancy)

                    citizenship = await CRUDCitizenShip.get(citizenship_id=get_vacancies[page].citizenship_id)
                    position = await CRUDPosition.get(position_id=get_vacancies[page].position_id)
                    city = await CRUDCity.get(city_id=get_vacancies[page].city_id)
                    work_experience = await CRUDWorkExperience.get(
                        work_experience_id=get_vacancies[page].work_experience_id)
                    english = await CRUDEnglish.get(english_id=get_vacancies[0].english_id)

                    vacancies_txt = f"В <b>Городе</b>: <u>{city.name}</u>\n" \
                                    f"Доступно вакансий: <b>{len(get_vacancies)}</b>\n" \
                                    f"Вакансия №{page + 1}\n" \
                                    f"<b>{position.name}</b>\n\n" \
                                    f"<b>Гражданство</b>: {citizenship.name}\n" \
                                    f"<b>Стаж</b>: {work_experience.name}\n" \
                                    f"<b>Знание английского языка</b>: {english.name}"

                    form = get_vacancies[page]
                    posting = TelegraphPage(CONFIG.TELEGRAPH)
                    url = await posting.create_page(form=form)
                    telegraph = f"<a href='{url['result']['url']}'>Подробнее</a>"

                    await callback.message.edit_text(
                        text=f"{vacancies_txt}\n{telegraph}",
                        reply_markup=await Profile.orders_iter_ikb(target="page_vacancies",
                                                                   page=int(page),
                                                                   user_id=callback.from_user.id,
                                                                   vacancies=get_vacancies
                                                                   ),
                        disable_web_page_preview=True
                    )

                # Пагинация для Откликов
                if data.get("target") == "page_responses":
                    page = int(data.get('id'))
                    vacancies = await CRUDVacancy.get_all()

                    responses = await CRUDApplicantReply.get_all(user_id=callback.from_user.id)

                    citizenship = await CRUDCitizenShip.get(citizenship_id=vacancies[page].citizenship_id)
                    position = await CRUDPosition.get(position_id=vacancies[page].position_id)
                    city = await CRUDCity.get(city_id=vacancies[page].city_id)
                    work_experience = await CRUDWorkExperience.get(
                        work_experience_id=vacancies[page].work_experience_id)
                    english = "Да" if vacancies[page].knowledge_of_english else "Нет"

                    status = responses[page].status_id
                    name_status = ""
                    if status == Statuses.Sent.value:
                        name_status = "<b>📨Отправлено📨</b>"
                    elif status == Statuses.Rejected.value:
                        name_status = "❌<b>Отклонено❌</b>"
                    elif status == Statuses.Review.value:
                        name_status = "<b>✉Приглашение✉</b>"
                    else:
                        name_status = "<b>✅Одобрено✅</b>"

                    vacancies_txt = f"Вы откликнулись на вакансию: <b>{position.name}</b>\n" \
                                    f"Статус отклика: {name_status}\n\n" \
                                    f"Вакансия №{page + 1}\n" \
                                    f"<b>{position.name}</b>\n\n" \
                                    f"<b>Город</b>: {city.name}\n" \
                                    f"<b>Гражданство</b>: {citizenship.name}\n" \
                                    f"<b>Стаж</b>: {work_experience.name}\n" \
                                    f"<b>Английский</b>: {english}\n"

                    await callback.message.edit_text(text=str(vacancies_txt),
                                                     reply_markup=await Profile.orders_iter_ikb(
                                                         target="page_responses",
                                                         page=int(page),
                                                         user_id=callback.from_user.id,
                                                         responses=True)
                                                     )

                # Редактирование
                if data.get("target") == "orderMenu":
                    current_user_id = data.get('id')
                    await callback.message.edit_text(
                        text="Редактирование",
                        reply_markup=await Profile.edit_ikb(current_user=int(current_user_id))
                    )
                    await state.finish()

                # Выбор что нужно редактировать
                if data.get("target") == "editQuestionnaire":
                    current_user_id = data.get('editId')
                    await callback.message.edit_text(
                        text="Выберите, что необходимо изменить",
                        reply_markup=await Profile.editQuestionnaire_ikb(current_user=int(current_user_id))
                    )

                # Вакансии
                if data.get("target") == "vacancies":

                    applicant_replies_id: list = list(
                        map(lambda x: x.vacancy_id, await CRUDApplicantReply.get_all(user_id=callback.from_user.id))
                    )

                    vacancies: list = await CRUDVacancy.get_all(is_published=True)
                    vacancies = list(filter(lambda x: x.id not in applicant_replies_id, vacancies))

                    get_vacancies: list = []
                    applicant_forms: list = await CRUDApplicantForm.get_all(user_id=callback.from_user.id)
                    for vacancy in vacancies:
                        for applicant_form in applicant_forms:
                            if vacancy.position_id == applicant_form.position_id:
                                get_vacancies.append(vacancy)

                    count = 0
                    if get_vacancies:
                        citizenship = await CRUDCitizenShip.get(citizenship_id=get_vacancies[0].citizenship_id)
                        position = await CRUDPosition.get(position_id=get_vacancies[0].position_id)
                        city = await CRUDCity.get(city_id=get_vacancies[0].city_id)
                        work_experience = await CRUDWorkExperience.get(
                            work_experience_id=get_vacancies[0].work_experience_id)
                        english = await CRUDEnglish.get(english_id=get_vacancies[0].english_id)

                        vacancies_txt = f"В <b>Городе</b>: <u>{city.name}</u>\n" \
                                        f"Доступно вакансий: <b>{len(get_vacancies)}</b>\n" \
                                        f"Вакансия №{count + 1}\n" \
                                        f"<b>{position.name}</b>\n\n" \
                                        f"<b>Гражданство</b>: {citizenship.name}\n" \
                                        f"<b>Стаж</b>: {work_experience.name}\n" \
                                        f"<b>Знание английского языка</b>: {english.name}" \

                        form = get_vacancies[0]
                        posting = TelegraphPage(CONFIG.TELEGRAPH)
                        url = await posting.create_page(form=form)
                        telegraph = f"<a href='{url['result']['url']}'>Подробнее</a>"

                        await callback.message.edit_text(text=f"{str(vacancies_txt)}\n{telegraph}",
                                                         reply_markup=await Profile.orders_iter_ikb(
                                                             target="page_vacancies",
                                                             user_id=callback.from_user.id,
                                                             vacancies=get_vacancies),
                                                         disable_web_page_preview=True
                                                         )
                    else:
                        await callback.answer("Активных вакансий нету")

                # Откликнуться на вакансию в меню "Вакансии"
                if data.get("target") == "response_vacancies":
                    vacancies_id = int(data.get('id'))
                    await CRUDApplicantReply.add(applicant_reply=ApplicantReplySchema(user_id=callback.from_user.id,
                                                                                      vacancy_id=vacancies_id,
                                                                                      status_id=Statuses.Sent.value))
                    applicant_replies_id: list = list(
                        map(lambda x: x.vacancy_id, await CRUDApplicantReply.get_all(user_id=callback.from_user.id))
                    )

                    vacancies: list = await CRUDVacancy.get_all(is_published=True)
                    vacancies = list(filter(lambda x: x.id not in applicant_replies_id, vacancies))

                    get_vacancies: list = []
                    applicant_forms: list = await CRUDApplicantForm.get_all(user_id=callback.from_user.id)
                    for vacancy in vacancies:
                        for applicant_form in applicant_forms:
                            if vacancy.position_id == applicant_form.position_id \
                                    and vacancy.city_id == applicant_form.city_id:
                                get_vacancies.append(vacancy)

                    count = 0
                    if get_vacancies:
                        citizenship = await CRUDCitizenShip.get(citizenship_id=get_vacancies[0].citizenship_id)
                        position = await CRUDPosition.get(position_id=get_vacancies[0].position_id)
                        city = await CRUDCity.get(city_id=get_vacancies[0].city_id)
                        work_experience = await CRUDWorkExperience.get(
                            work_experience_id=get_vacancies[0].work_experience_id)
                        english = "Да" if get_vacancies[0].knowledge_of_english else "Нет"

                        vacancies_txt = f"В <b>Городе</b>: <u>{city.name}</u>\n" \
                                        f"Доступно вакансий: <b>{len(get_vacancies)}</b>\n" \
                                        f"Вакансия №{count + 1}\n" \
                                        f"<b>{position.name}</b>\n\n" \
                                        f"<b>Гражданство</b>: {citizenship.name}\n" \
                                        f"<b>Стаж</b>: {work_experience.name}\n" \
                                        f"<b>Английский</b>: {english.name}\n"

                        form = get_vacancies[0]
                        posting = TelegraphPage(CONFIG.TELEGRAPH)
                        url = await posting.create_page(form=form)
                        telegraph = f"<a href='{url['result']['url']}'>Подробнее</a>"

                        await callback.message.edit_text(text=f"Вы успешно откликнулись на вакансию\n"
                                                              f"{str(vacancies_txt)}\n{telegraph}",
                                                         reply_markup=await Profile.orders_iter_ikb(
                                                             target="page_vacancies",
                                                             user_id=callback.from_user.id,
                                                             vacancies=get_vacancies),
                                                         disable_web_page_preview=True
                                                         )
                    else:
                        await callback.message.edit_text(text="Вы успешно откликнулись на вакансию",
                                                         reply_markup=await Profile.profile_ikb(
                                                             user_id=callback.from_user.id)
                                                         )

                # Мои отклики в "Профиле"
                if data.get("target") == "responses":
                    responses = await CRUDApplicantReply.get_all(user_id=callback.from_user.id)
                    vacancies = await CRUDVacancy.get_all()

                    if responses:
                        citizenship = await CRUDCitizenShip.get(citizenship_id=vacancies[0].citizenship_id)
                        position = await CRUDPosition.get(position_id=vacancies[0].position_id)
                        city = await CRUDCity.get(city_id=vacancies[0].city_id)
                        work_experience = await CRUDWorkExperience.get(
                            work_experience_id=vacancies[0].work_experience_id)

                        english = await CRUDEnglish.get(english_id=vacancies[0].english_id)

                        status = responses[0].status_id
                        name_status = ""
                        if status == Statuses.Sent.value:
                            name_status = "<b>📨Отправлено📨</b>"
                        elif status == Statuses.Rejected.value:
                            name_status = "❌<b>Отклонено❌</b>"
                        elif status == Statuses.Review.value:
                            name_status = "<b>✉Приглашение✉</b>"
                        else:
                            name_status = "<b>✅Одобрено✅</b>"

                        count = 0
                        vacancies_txt = f"Вы откликнулись на вакансию: <b>{position.name}</b>\n" \
                                        f"Статус отклика: {name_status}\n\n" \
                                        f"Вакансия №{count + 1}\n" \
                                        f"<b>{position.name}</b>\n\n" \
                                        f"<b>Город</b>: {city.name}\n" \
                                        f"<b>Гражданство</b>: {citizenship.name}\n" \
                                        f"<b>Стаж</b>: {work_experience.name}\n" \
                                        f"<b>Английский</b>: {english.name}\n"

                        await callback.message.edit_text(text=str(vacancies_txt),
                                                         reply_markup=await Profile.orders_iter_ikb(
                                                             target="page_responses",
                                                             user_id=callback.from_user.id,
                                                             responses=True)
                                                         )
                    else:
                        await callback.answer(text="Вы не откликались на вакансии")

                # Опубликовать
                if data.get("target") == "publishQuestionnaire":
                    current_user_id = int(data.get('editId'))
                    user = await CRUDApplicantForm.get(applicant_form_id=current_user_id)
                    user.is_published = True
                    await CRUDApplicantForm.update(applicant_form=user)
                    await callback.message.edit_text("Редактирование\nАнкета опубликована",
                                                     reply_markup=await Profile.edit_ikb(
                                                         current_user=int(current_user_id)))

                # Скрыть
                if data.get("target") == "hideQuestionnaire":
                    current_user_id = int(data.get('editId'))
                    user = await CRUDApplicantForm.get(applicant_form_id=current_user_id)
                    user.is_published = False
                    await CRUDApplicantForm.update(applicant_form=user)
                    await callback.message.edit_text("Редактирование\nАнкета скрыта",
                                                     reply_markup=await Profile.edit_ikb(current_user=current_user_id))

                # Удаление анкеты
                if data.get("target") == "deleteQuestionnaire":
                    applicant_form_id = int(data.get('editId'))
                    await CRUDRecentJob.delete(applicant_form_id=applicant_form_id)
                    await CRUDApplicantForm.delete(applicant_form_id=applicant_form_id)
                    if await CRUDUser.get(user_id=callback.from_user.id) is None:
                        await callback.answer("Анкета удалена")
                    else:
                        await callback.message.edit_text(text="У вас больше нет анкет\n"
                                                              "Главное меню",
                                                         reply_markup=await Profile.profile_ikb(callback.from_user.id))

                if data.get("target") == "support":
                    text = f"\n\n" \
                           f"📱 Контактный номер телефона : {CONFIG.SUPPORT.PHONE}\n\n" \
                           f"📧 Email: {CONFIG.SUPPORT.EMAIL}\n\n" \
                           f"📷 Instagram : <a href='www.instagram.com/{CONFIG.SUPPORT.INSTAGRAM}/'>{CONFIG.SUPPORT.INSTAGRAM}</a>\n\n" \
                           f"🎧 Discord :<code>{CONFIG.SUPPORT.DISCORD}</code>\n\n"
                    await callback.message.edit_text(text=f"Способ связи: {text}",
                                                     reply_markup=await Profile.support_ikb(),
                                                     parse_mode="HTML")

                if data.get("target") == "scheduler":
                    approve = int(data.get('id'))
                    user_id = int(data.get('editId'))
                    if approve == 1:
                        applicant_form = await CRUDApplicantForm.get(user_id=user_id)
                        applicant_form.date_created = datetime.now()
                        await CRUDApplicantForm.update(applicant_form=applicant_form)
                        await callback.answer(text="Данные успешно обновлены")
                    else:
                        applicant_form = await CRUDApplicantForm.get(user_id=user_id)
                        applicant_form.is_published = False
                        applicant_form.date_created = datetime.now()
                        await CRUDApplicantForm.update(applicant_form=applicant_form)
                        await callback.answer(text="Данные успешно обновлены")
                    print('ads')

                if data.get("target") == "Edit":
                    edit_id = int(data.get('id'))
                    # Фамилия+
                    if edit_id == 0:
                        applicant_form_id = int(data.get("editId"))
                        await state.update_data(applicant_form_id=applicant_form_id)
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        text = f"Фамилия: <b>{user.surname}</b>\n\n" \
                               f"Введите Фамилию"
                        await EditProfile.Surname.set()
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await Profile.back(
                                                             user_id=applicant_form_id)
                                                         )
                    # Имя+
                    if edit_id == 1:
                        applicant_form_id = int(data.get("editId"))
                        await state.update_data(applicant_form_id=applicant_form_id)
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        text = f"Имя: <b>{user.name}</b>\n\n" \
                               f"Введите Имя"
                        await EditProfile.Name.set()
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await Profile.back(
                                                             user_id=applicant_form_id)
                                                         )
                    # Отчество+
                    if edit_id == 2:
                        applicant_form_id = int(data.get("editId"))
                        await state.update_data(applicant_form_id=applicant_form_id)
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        text = f"Отчество: <b>{user.patronymic}</b>\n\n" \
                               f"Введите Отчество"
                        await EditProfile.Patronymic.set()
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await Profile.back(
                                                             user_id=applicant_form_id)
                                                         )
                    # Дата рождения
                    if edit_id == 3:
                        applicant_form_id = int(data.get("editId"))
                        await state.update_data(applicant_form_id=applicant_form_id)
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)

                        date_date_of_birth: str = f"{str(user.date_of_birth.day)}." \
                                                  f"{str(user.date_of_birth.month)}." \
                                                  f"{str(user.date_of_birth.year)}"

                        text = f"Дата рождения: <b>{date_date_of_birth}</b>\n\n" \
                               f"Выберите дату рождения"
                        await EditProfile.DateOfBirth.set()
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await DialogCalendar().start_calendar()
                                                         )
                    # Гражданство+
                    if edit_id == 4:
                        applicant_form_id = int(data.get("editId"))
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        citizenship = await CRUDCitizenShip.get(citizenship_id=user.citizenship_id)
                        text = f"Гражданство: <b>{citizenship.name}</b>\n\n" \
                               f"Выберите новое гражданство"
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await Profile.citizenship_ikb(
                                                             user_id=applicant_form_id)
                                                         )
                        await state.update_data(examination=applicant_form_id)
                        await state.update_data(edit_id=edit_id)
                        await EditProfile.Examination.set()
                    # Телефон+
                    if edit_id == 5:
                        await callback.message.delete()
                        await state.update_data(applicant_form_id=int(data.get("editId")))
                        user = await CRUDApplicantForm.get(applicant_form_id=int(data.get("editId")))
                        phone = ""
                        if user.phone_number is None:
                            phone: str = 'N/A'
                        text = f"Номер телефона: <b>{phone}</b>\n\n" \
                               f"Введите новый номер телфона"
                        await callback.message.answer(text=text, reply_markup=await Profile.send_contact_ikb(
                            user_id=int(data.get("editId"))))
                        await EditProfile.PhoneNumber.set()
                    # Город+
                    if edit_id == 6:
                        applicant_form_id = int(data.get("editId"))
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        city = await CRUDCity.get(city_id=user.city_id)
                        text = f"Город: <i>{city.name}</i>\n\n" \
                               f"Изменить город"
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await Profile.cities_ikb(
                                                             user_id=applicant_form_id)
                                                         )
                        await state.update_data(examination=applicant_form_id)
                        await state.update_data(edit_id=edit_id)
                        await EditProfile.Examination.set()

                    # Семейное положение+
                    if edit_id == 7:
                        applicant_form_id = int(data.get("editId"))
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        married_txt = "Да" if user.is_married else 'Нет'
                        text = f"Вы Замужем\Женаты: <i>{married_txt}</i>\n\n" \
                               f"Изменить"

                        await callback.message.edit_text(
                            text=text,
                            reply_markup=await Profile.approve_ikb(target="MarriedEdit", user_id=applicant_form_id)
                        )
                        await state.update_data(examination=applicant_form_id)
                        await state.update_data(edit_id=edit_id)
                        await EditProfile.Examination.set()
                    # Инстаграм+
                    if edit_id == 8:
                        applicant_form_id = int(data.get("editId"))
                        await state.update_data(applicant_form_id=applicant_form_id)
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        insta: str = ''
                        if user.instagram_url is None:
                            insta: str = 'N/A'
                        await EditProfile.InstagramUrl.set()
                        text = f"Интаграм: <b>{insta}</b>\n\n" \
                               f"Введите Инстаграм"
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await Profile.back(
                                                             user_id=applicant_form_id)
                                                         )
                    # Английский+
                    if edit_id == 9:
                        applicant_form_id = int(data.get("editId"))
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        english_edit = await CRUDEnglish.get(english_id=user.knowledge_of_english)

                        text = f"Английский: <i>{english_edit.name}</i>\n\n" \
                               f"Выберите знание английского языка"

                        await callback.message.edit_text(
                            text=text,
                            reply_markup=await Profile.english_ikb(user_id=applicant_form_id)
                        )
                        await state.update_data(examination=applicant_form_id)
                        await state.update_data(edit_id=edit_id)
                        await EditProfile.Examination.set()
                    # Стаж+
                    if edit_id == 10:
                        applicant_form_id = int(data.get("editId"))
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        work_experience = await CRUDWorkExperience.get(work_experience_id=user.work_experience_id)
                        text = f"Стаж: <b><i>{work_experience.name}</i></b>\n\n" \
                               f"Выберите новый стаж"
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await Profile.work_experience_ikb(
                                                             user_id=applicant_form_id)
                                                         )
                        await state.update_data(examination=applicant_form_id)
                        await state.update_data(edit_id=edit_id)
                        await EditProfile.Examination.set()
                    # Желаемое место работы
                    if edit_id == 11:
                        applicant_form_id = int(data.get("editId"))
                        user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                        position = await CRUDPosition.get(position_id=user.position_id)
                        text = f"Желаемое место работы : <i>{position.name}</i>\n\n" \
                               f"Выберите новое желаемое место работы"

                        await callback.message.edit_text(text=text,
                                                         reply_markup=await Profile.position_ikb(
                                                             user_id=applicant_form_id)
                                                         )
                        await state.update_data(examination=applicant_form_id)
                        await state.update_data(edit_id=edit_id)
                        await EditProfile.Examination.set()
                    # Последнее места работы
                    if edit_id == 12:
                        applicant_form_id = int(data.get("editId"))
                        await EditProfile.RecentJob.set()
                        await state.update_data(applicant_form_id=applicant_form_id)
                        await callback.message.edit_text(text="Последние места работы",
                                                         reply_markup=await Profile.recent_job_ikb(
                                                             recent_job_id=int(applicant_form_id),
                                                             user_id=int(applicant_form_id))
                                                         )
                        await state.update_data(examination=applicant_form_id)
                        await state.update_data(edit_id=edit_id)
                        await EditProfile.Examination.set()

                if data.get("target") == "SubpositionsEdit":
                    position_id = int(data.get('id'))
                    applicant_form_id = int(data.get("editId"))
                    user = await CRUDApplicantForm.get(applicant_form_id=applicant_form_id)
                    position = await CRUDPosition.get(position_id=user.position_id)
                    text = f"Желаемое место работы : <i>{position.name}</i>\n\n" \
                           f"Выберите новое желаемое место работы"

                    await callback.message.edit_text(text=text,
                                                     reply_markup=await Profile.subpositions_ikb(
                                                         position_id=position_id,
                                                         user_id=applicant_form_id)
                                                     )
                if data.get("target") == "RecentJob":
                    current_user_id = data.get("editId")
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(current_user_id))
                    subposition_id = int(data.get('id'))
                    applicant_form.position_id = subposition_id

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Желаемая должность изменена",
                                                     reply_markup=await Profile.editQuestionnaire_ikb(
                                                         current_user=int(current_user_id))
                                                     )
                if data.get("target") == "cityEdit":
                    current_user_id = data.get("editId")
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(current_user_id))
                    city_id = int(data.get('id'))
                    applicant_form.city_id = city_id

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Город изменен",
                                                     reply_markup=await Profile.editQuestionnaire_ikb(
                                                         current_user=int(current_user_id))
                                                     )
                if data.get("target") == "MarriedEdit":
                    current_user_id = data.get("editId")
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(current_user_id))
                    married_id = int(data.get('id'))
                    result = True if married_id == 1 else False
                    applicant_form.is_married = result

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Семейное положение изменено",
                                                     reply_markup=await Profile.editQuestionnaire_ikb(
                                                         current_user=int(current_user_id))
                                                     )
                if data.get("target") == "EnglishEdit":
                    current_user_id = data.get("editId")
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(current_user_id))
                    english_id = int(data.get('id'))
                    applicant_form.knowledge_of_english = english_id

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Английский язык изменен",
                                                     reply_markup=await Profile.editQuestionnaire_ikb(
                                                         current_user=int(current_user_id))
                                                     )
                if data.get("target") == "WorkExperienceEdit":
                    current_user_id = data.get("editId")
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(current_user_id))
                    work_experience_id = int(data.get('id'))
                    applicant_form.work_experience_id = work_experience_id

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Стаж работы изменен",
                                                     reply_markup=await Profile.editQuestionnaire_ikb(
                                                         current_user=int(current_user_id))
                                                     )
                if data.get("target") == "CitizenshipEdit":
                    current_user_id = data.get("editId")
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(current_user_id))
                    citizenship_id = int(data.get('id'))
                    applicant_form.citizenship_id = citizenship_id

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Гражданство изменено",
                                                     reply_markup=await Profile.editQuestionnaire_ikb(
                                                         current_user=int(current_user_id))
                                                     )
                if data.get("target") == "addRecentJob":
                    current_user_id = int(data.get("editId"))

                    await EditProfile.RecentJob.set()
                    await callback.message.edit_text(text="Введите место работы",
                                                     reply_markup=await Profile.back(user_id=current_user_id))
                if data.get("target") == "DelrecentJob":
                    current_user_id = int(data.get("editId"))
                    current_user = int(data.get("id"))
                    await CRUDRecentJob.delete(recent_job_id=current_user)
                    await callback.message.edit_text(text="Место работы <b>удалено</b>",
                                                     reply_markup=await Profile.recent_job_ikb(
                                                         recent_job_id=int(current_user_id),
                                                         user_id=int(current_user_id))
                                                     )
                if data.get("target") == "recentJobEdit":
                    current_user_id = int(data.get("editId"))
                    data_edit = await state.get_data()
                    await state.update_data(edit_id=int(data.get("id")))
                    data_edit["edit_id"] = data.get("id")
                    await EditProfile.RecentJobEdit.set()
                    await callback.message.edit_text(text="Введите место работы",
                                                     reply_markup=await Profile.back(user_id=current_user_id))

            elif callback.data.startswith("dialog_calendar"):
                data = calendar_callback.parse(callback_data=callback.data)
                date_of_birth = datetime(year=int(data.get("year")), day=int(data.get("day")),
                                         month=int(data.get("month")))

                applicant_form_id = await state.get_data()
                applicant_form = await CRUDApplicantForm.get(
                    applicant_form_id=int(applicant_form_id['applicant_form_id']))
                applicant_form.date_of_birth = date_of_birth

                await CRUDApplicantForm.update(applicant_form=applicant_form)
                await callback.message.edit_text(text="Дата рождения изменена\nГлавное меню",
                                                 reply_markup=await Profile.editQuestionnaire_ikb(
                                                     current_user=int(applicant_form_id['applicant_form_id']))
                                                 )
        if message:
            await message.delete()

            try:
                await bot.delete_message(
                    chat_id=message.from_user.id,
                    message_id=message.message_id - 1
                )
            except BadRequest:
                pass

            if state:
                if await state.get_state() == "EditProfile:Surname":
                    data = await state.get_data()
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form_id"]))
                    applicant_form.surname = message.text
                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await message.answer(text="Фамилия изменена", reply_markup=await Profile.editQuestionnaire_ikb(
                        current_user=int(data["applicant_form_id"]))
                                         )
                    await state.finish()
                if await state.get_state() == "EditProfile:Name":
                    data = await state.get_data()
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form_id"]))
                    applicant_form.name = message.text
                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await message.answer(text="Имя изменено", reply_markup=await Profile.editQuestionnaire_ikb(
                        current_user=int(data["applicant_form_id"]))
                                         )
                    await state.finish()
                if await state.get_state() == "EditProfile:Patronymic":
                    data = await state.get_data()
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form_id"]))
                    applicant_form.patronymic = message.text
                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await message.answer(text="Отчество изменено", reply_markup=await Profile.editQuestionnaire_ikb(
                        current_user=int(data["applicant_form_id"]))
                                         )
                    await state.finish()
                if await state.get_state() == "EditProfile:InstagramUrl":
                    data = await state.get_data()
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form_id"]))
                    applicant_form.instagram_url = message.text
                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await message.answer(text="Инстаграм изменен", reply_markup=await Profile.editQuestionnaire_ikb(
                        current_user=int(data["applicant_form_id"]))
                                         )
                    await state.finish()

                if await state.get_state() == "EditProfile:PhoneNumber":
                    data = await state.get_data()
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form_id"]))

                    if message.content_type == "contact":
                        examination_phone = re.findall(r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})',
                                                       message.contact.phone_number)
                        if examination_phone:
                            applicant_form.phone_number = message.contact.phone_number

                            await CRUDApplicantForm.update(applicant_form=applicant_form)
                            await message.answer(text="Телефон изменен",
                                                 reply_markup=await Profile.editQuestionnaire_ikb(
                                                     current_user=int(data["applicant_form_id"]))
                                                 )
                            await state.finish()
                        else:
                            await EditProfile.PhoneNumber.set()
                            await message.answer(
                                text='Вы ввели не верный формат телефона\n'
                                     'Пример (+7 000 000 00 00) без пробелов',
                                reply_markup=await Profile.send_contact_ikb(user_id=message.from_user.id)
                            )
                    elif message.text == "Назад":
                        await message.answer(text="Редактирование", reply_markup=await Profile.editQuestionnaire_ikb(
                            current_user=int(data["applicant_form_id"]))
                                             )
                        await state.finish()
                    else:
                        applicant_form.phone_number = message.text

                        await CRUDApplicantForm.update(applicant_form=applicant_form)
                        await message.answer(text="Телефон изменен", reply_markup=await Profile.editQuestionnaire_ikb(
                            current_user=int(data["applicant_form_id"]))
                                                 )
                        await state.finish()
                # сделать state.finish
                if await state.get_state() == "EditProfile:RecentJob":
                    data = await state.get_data()
                    await CRUDRecentJob.add(
                        recent_job=RecentJobSchema(name=message.text,
                                                   applicant_form_id=int(data['applicant_form_id'])))
                    await message.answer(text="Место работы добавлено", reply_markup=await Profile.recent_job_ikb(
                        recent_job_id=int(data["applicant_form_id"]),
                        user_id=int(data["applicant_form_id"])))

                if await state.get_state() == "EditProfile:RecentJobEdit":
                    data_edit = await state.get_data()
                    recent_job = await CRUDRecentJob.get(recent_job_id=int(data_edit.get("edit_id")))
                    recent_job.name = message.text

                    await CRUDRecentJob.update(recent_job=recent_job)
                    await message.answer(text="Место работы добавлено", reply_markup=await Profile.recent_job_ikb(
                        recent_job_id=int(data_edit["applicant_form_id"]),
                        user_id=int(data_edit["applicant_form_id"])))

                if await state.get_state() == "EditProfile:Examination":
                    data = await state.get_data()
                    if int(data["edit_id"]) == 4:
                        if message.text:
                            user = await CRUDApplicantForm.get(applicant_form_id=int(data["examination"]))
                            citizenship = await CRUDCitizenShip.get(citizenship_id=user.citizenship_id)
                            await message.answer(
                                text=f"Гражданство: <b>{citizenship.name}</b>\n\n"
                                     f"Выберите из списка",
                                reply_markup=await Profile.citizenship_ikb(user_id=int(data["examination"]))
                            )
                    if int(data["edit_id"]) == 6:
                        if message.text:
                            user = await CRUDApplicantForm.get(applicant_form_id=int(data["examination"]))
                            city = await CRUDCity.get(city_id=user.city_id)
                            await message.answer(text=f"Город: <i>{city.name}</i>\n\n" \
                                                      f"Выберите из списка",
                                                 reply_markup=await Profile.cities_ikb(user_id=int(data["examination"]))
                                                 )
                    if int(data["edit_id"]) == 7:
                        if message.text:
                            user = await CRUDApplicantForm.get(applicant_form_id=int(data["examination"]))
                            married_txt = "Да" if user.is_married else 'Нет'
                            text = f"Вы Замужем\Женаты: <i>{married_txt}</i>\n\n" \
                                   f"Выберите из списка"

                            await message.answer(text=text,
                                                 reply_markup=await Profile.approve_ikb(
                                                     target="MarriedEdit",
                                                     user_id=int(data["examination"]))
                                                 )
                    if int(data["edit_id"]) == 9:
                        # user = await CRUDApplicantForm.get(applicant_form_id=int(data["examination"]))
                        # english_txt = "Да" if user.knowledge_of_english else "Нет"
                        # text = f"Английский: <i>{english_txt}</i>\n\n" \
                        #        f"Выберите владеете ли вы английским языком"

                        await message.answer(text="Выберите из списка",
                                             reply_markup=await Profile.approve_ikb(
                                                 target="EnglishEdit",
                                                 user_id=int(data["examination"]))
                                             )
                    if int(data["edit_id"]) == 10:
                        await message.answer(text="Выберите стаж из списка",
                                             reply_markup=await Profile.work_experience_ikb(
                                                 user_id=int(data["examination"]))
                                             )
                    if int(data["edit_id"]) == 11:
                        user = await CRUDApplicantForm.get(applicant_form_id=int(data["examination"]))
                        position = await CRUDPosition.get(position_id=user.position_id)
                        text = f"Желаемое место работы : <i>{position.name}</i>\n\n" \
                               f"Выберите новое желаемое место работы"

                        await message.answer(text=text,
                                             reply_markup=await Profile.position_ikb(
                                                 user_id=int(data["examination"]))
                                             )
                    if int(data["edit_id"]) == 12:
                        await message.answer(text="Последние места работы",
                                             reply_markup=await Profile.recent_job_ikb(
                                                 recent_job_id=int(int(data["examination"])),
                                                 user_id=int(int(data["examination"])))
                                             )
                        await state.finish()
