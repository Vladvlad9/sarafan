from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest
from pydantic import ValidationError

from crud.applicant_forms import CRUDApplicantForm
from crud.citizenship import CRUDCitizenShip
from crud.english import CRUDEnglish
from crud.position import CRUDPosition
from crud.recent_jobs import CRUDRecentJob
from crud.users import CRUDUser
from crud.work_experiences import CRUDWorkExperience
from enums import Roles
from keyboards.inline.users.сalendar import DialogCalendar, calendar_callback
from loader import bot
from schemas import ApplicantFormSchema, RecentJobSchema, UserSchema
from states.users import UserRegister, EditRegister

register_cb = CallbackData("reg", "target", "id", "editId")
profile_cb = CallbackData("profile", "target", "id", "editId")


class Register:
    @staticmethod
    async def back() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="← Назад",
                                         callback_data=register_cb.new("editQuestionnaire", 0, 0))
                ]
            ]
        )

    @staticmethod
    async def back_registration(target: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data=profile_cb.new(target, 0,
                                                                      0))
                ]
            ]
        )

    @staticmethod
    async def cancel_ikb(target: str = None) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад", callback_data=register_cb.new(target, 0, 0))
                ]
            ]
        )

    @staticmethod
    async def profile_ikb(user_id: int, registration: bool = None) -> InlineKeyboardMarkup:
        count = 0
        if registration:
            count = 5
        vacancies = await CRUDApplicantForm.get(user_id=user_id)

        date_of_birth_ikb = [InlineKeyboardButton(text="Заполнить анкету",
                                                  callback_data=register_cb.new("date_of_birth", count, 0))]
        my_questionnaires_ikb = [InlineKeyboardButton(text="Мои анкеты",
                                                      callback_data=profile_cb.new("my_questionnaires", 1, 0))]
        responses_ikb = [InlineKeyboardButton(text="Мои отклики",
                                              callback_data=profile_cb.new("responses", 1, 0))]
        vacancies_ikb = [InlineKeyboardButton(text="Вакансии",
                                              callback_data=profile_cb.new("vacancies", 1, 0))]
        support_ikb = [InlineKeyboardButton(text="Поддержка", callback_data=profile_cb.new("support", 1, user_id))]
        if vacancies:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    date_of_birth_ikb, my_questionnaires_ikb, responses_ikb, vacancies_ikb, support_ikb
                ]
            )
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    date_of_birth_ikb, my_questionnaires_ikb, responses_ikb, support_ikb
                ]
            )
        return keyboard

    @staticmethod
    async def skip_ikb(target: str, registration: bool = None, targetBack: str = None) -> InlineKeyboardMarkup:
        if registration:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Пропустить', callback_data=register_cb.new(target, 0, 0))
                    ]
                ]
            )
        else:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Пропустить', callback_data=register_cb.new(target, 0, 0)),
                        InlineKeyboardButton(text='Назад', callback_data=register_cb.new(targetBack, 0, 0))
                    ]
                ]
            )

    @staticmethod
    async def send_contact(registration: bool = None, targetBack: str = None) -> ReplyKeyboardMarkup:
        if registration:
            return ReplyKeyboardMarkup(
                row_width=4,
                resize_keyboard=True,
                one_time_keyboard=True,
                keyboard=[
                    [
                        KeyboardButton(text='Поделиться контактом',
                                       request_contact=True),
                        KeyboardButton(text='Пропустить', callback_data=register_cb.new("PhoneNumber", 0, 0))
                    ]
                ]
            )
        else:
            return ReplyKeyboardMarkup(
                row_width=4,
                resize_keyboard=True,
                one_time_keyboard=True,
                keyboard=[
                    [
                        KeyboardButton(text='Поделиться контактом',
                                       request_contact=True),
                        KeyboardButton(text='Пропустить', callback_data=register_cb.new("PhoneNumber", 0, 0)),
                        KeyboardButton(text='Назад', callback_data=register_cb.new(targetBack, 0, 0))
                    ]
                ]
            )

    @staticmethod
    async def start() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Заполнить анкету",
                        callback_data=register_cb.new("date_of_birth", 0, 0)
                    )
                ]
            ]
        )

    @staticmethod
    async def approve_ikb(target: str, registration: bool = None) -> InlineKeyboardMarkup:
        if registration:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Да", callback_data=register_cb.new(target, 1, 0)),
                        InlineKeyboardButton(text="Нет", callback_data=register_cb.new(target, 0, 0))
                    ]
                ]
            )
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Да", callback_data=register_cb.new(target, 1, 0)),
                        InlineKeyboardButton(text="Нет", callback_data=register_cb.new(target, 0, 0))
                    ]
                ]
            )
        return keyboard

    @staticmethod
    async def position_ikb(CRUD,
                           target: str = None,
                           postion: bool = None,
                           subpositions_id: int = None,
                           registration: bool = None,
                           edit: bool = None,
                           targetBack: str = None,
                           position_edit: bool = None,
                           subpositions_edit_id: int = None,
                           targetNext: str = None):
        if edit:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=name.name,
                                                             callback_data=register_cb.new(target, name.id, 0))
                                    ]
                                    for name in await CRUD.get_all()
                                ] + [
                                    [
                                        InlineKeyboardButton(text='Назад',
                                                             callback_data=register_cb.new("editQuestionnaire", 0, 0))
                                    ]
                                ]
            )
        elif registration:
            if postion:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=name.name,
                                                                 callback_data=register_cb.new(target, name.id, 0))
                                        ]
                                        for name in await CRUD.get_all(position=True)
                                    ] + [
                                        [
                                            InlineKeyboardButton(text="Назад",
                                                                 callback_data=register_cb.new(targetBack, 0, 0))
                                        ]
                                    ]
                )
            elif subpositions_id:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=name.name,
                                                                 callback_data=register_cb.new(target, name.id, 0))
                                        ]
                                        for name in await CRUD.get_all(subpositions_id=subpositions_id)
                                    ] + [
                                        [
                                            InlineKeyboardButton(text='Продолжить',
                                                                 callback_data=register_cb.new(targetNext, 0, 0)),
                                            InlineKeyboardButton(text='Назад',
                                                                 callback_data=register_cb.new(targetBack, 0, 0))
                                        ]
                                    ]
                )
            else:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=name.name,
                                                                 callback_data=register_cb.new(target, name.id, 0))
                                        ]
                                        for name in await CRUD.get_all()
                                    ] + [
                                        [
                                            InlineKeyboardButton(text='Назад',
                                                                 callback_data=register_cb.new(targetBack, 0, 0))
                                        ]
                                    ]
                )
        else:
            if postion:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=name.name,
                                                                 callback_data=register_cb.new(target, name.id, 0))
                                        ]
                                        for name in await CRUD.get_all(position=True)
                                    ] + [
                                        [
                                            InlineKeyboardButton(text="Назад",
                                                                 callback_data=register_cb.new(targetBack, 0, 0))
                                        ]
                                    ]
                )
            elif position_edit:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=name.name,
                                                                 callback_data=register_cb.new(target, name.id, 0))
                                        ]
                                        for name in await CRUD.get_all(position=True)
                                    ]
                )
            elif subpositions_edit_id:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [InlineKeyboardButton(text=name.name,
                                                              callback_data=register_cb.new(target, name.id, 0))
                                         ]
                                        for name in await CRUD.get_all(subpositions_id=subpositions_edit_id)
                                    ]
                )
            elif subpositions_id:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=name.name,
                                                                 callback_data=register_cb.new(target, name.id, 0))
                                         ]

                                        for name in await CRUD.get_all(subpositions_id=subpositions_id)
                                    ] + [
                                        [
                                            InlineKeyboardButton(text="Назад",
                                                                 callback_data=register_cb.new(targetBack, 0, 0))
                                        ]
                                    ]
                )
            else:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [InlineKeyboardButton(text=name.name,
                                                              callback_data=register_cb.new(target, name.id, 0))
                                         ]
                                        for name in await CRUD.get_all()
                                    ] + [
                                        [
                                            InlineKeyboardButton(text='Назад',
                                                                 callback_data=register_cb.new(targetBack, 0, 0))
                                        ]
                                    ]
                )

    @staticmethod
    async def editQuestionnaire_ikb(data: dict = None) -> InlineKeyboardMarkup:
        data_user: dict = data

        applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data.get("applicant_form")))
        citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form.citizenship_id)
        work_experience = await CRUDWorkExperience.get(work_experience_id=applicant_form.work_experience_id)
        # position = await CRUDPosition.get(position_id=data_user["position_id"])
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
            phone = applicant_form.phone_number

        if applicant_form.instagram_url is None:
            insta: str = 'N/A'
        else:
            insta = applicant_form.instagram_url

        date_date_of_birth: str = str(applicant_form.date_of_birth.day) + "." \
                                  + str(applicant_form.date_of_birth.month) + "." \
                                  + str(applicant_form.date_of_birth.year)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"Фамилия➛ {data_user['surname']}",
                                         callback_data=register_cb.new("Edit", 0, 0))
                ],
                [
                    InlineKeyboardButton(text=f"Имя➛ {data_user['name']}",
                                         callback_data=register_cb.new("Edit", 1, 0)),
                ],
                [
                    InlineKeyboardButton(text=f"Отчество➛ {patronymic}", callback_data=register_cb.new("Edit", 2, 0)),
                ],
                [
                    InlineKeyboardButton(text=f"Дата рождения➛ {date_date_of_birth}",
                                         callback_data=register_cb.new("Edit", 3, 0))
                ],
                [
                    InlineKeyboardButton(text=f"Гражданство➛ {citizenship.name}",
                                         callback_data=register_cb.new("Edit", 4, 0))
                ],
                [
                    InlineKeyboardButton(text=f"Телефон➛ {phone}",
                                         callback_data=register_cb.new("Edit", 5, 0))
                ],
                [
                    InlineKeyboardButton(text=f"Инстаграм➛ {insta}",
                                         callback_data=register_cb.new("Edit", 6, 0))
                ],
                [
                    InlineKeyboardButton(text=f"Английский➛ {knowledge_of_english.name}",
                                         callback_data=register_cb.new("Edit", 7, 0))
                ],
                [
                    InlineKeyboardButton(text=f"Стаж➛ {work_experience.name}",
                                         callback_data=register_cb.new("Edit", 8, 0))
                ],
                [
                    InlineKeyboardButton(text=f"Желаемое место работы",
                                         callback_data=register_cb.new("Edit", 9, 0))
                ],
                [
                    InlineKeyboardButton(text=f"Последние места работы",
                                         callback_data=register_cb.new("Edit", 10, 0))
                ],

                [InlineKeyboardButton(text="← Назад",
                                      callback_data=register_cb.new("next", 11, 0))],
            ]
        )
        return keyboard

    @staticmethod
    async def work_experience_ikb(registration: bool = None, edit: bool = None,
                                  targetBack: str = None) -> InlineKeyboardMarkup:
        if edit:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=work_experience.name,
                                                             callback_data=register_cb.new("WorkExperienceEdit",
                                                                                           work_experience.id, 0)
                                                             )
                                    ]
                                    for work_experience in await CRUDWorkExperience.get_all()
                                ] + [
                                    [
                                        InlineKeyboardButton(text="←Назад",
                                                             callback_data=register_cb.new("editQuestionnaire", 0,
                                                                                           0))
                                    ]
                                ]
            )
        elif registration:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=work_experience.name,
                                             callback_data=register_cb.new("WorkExperienceId", work_experience.id, 0))
                    ]
                    for work_experience in await CRUDWorkExperience.get_all()
                ]
            )
        else:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=work_experience.name,
                                                             callback_data=register_cb.new("WorkExperienceId",
                                                                                           work_experience.id, 0)
                                                             )

                                    ] for work_experience in await CRUDWorkExperience.get_all()
                                ] + [
                                    [
                                        InlineKeyboardButton(text='Назад',
                                                             callback_data=register_cb.new(targetBack, 0, 0))
                                    ]
                                ]
            )

    @staticmethod
    async def english_ikb(target: str = None, registration: bool = None, edit: bool = None,
                          targetBack: str = None) -> InlineKeyboardMarkup:

        if edit:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=english.name,
                                                             callback_data=register_cb.new(target, english.id, 0))
                                    ]
                                    for english in await CRUDEnglish.get_all()
                                ] + [
                                    [
                                        InlineKeyboardButton(text='Назад',
                                                             callback_data=register_cb.new("editQuestionnaire", 0, 0))
                                    ]
                                ]
            )
        elif registration:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    InlineKeyboardButton(text=english.name,
                                         callback_data=register_cb.new("English", english.id, 0))
                    for english in await CRUDEnglish.get_all()
                ]
            )
        else:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=english.name,
                                                             callback_data=register_cb.new("English", english.id, 0))
                                    ]
                                    for english in await CRUDEnglish.get_all()
                                ] + [
                                    [
                                        InlineKeyboardButton(text='Назад',
                                                             callback_data=register_cb.new(targetBack, 0, 0))
                                    ]
                                ]
            )

    @staticmethod
    async def recent_job_ikb(recent_job_id: int, edit: int = None, targetBack: str = None) -> InlineKeyboardMarkup:
        recent_job = await CRUDRecentJob.get_name(recent_job_id=recent_job_id)

        if edit:
            keyboards = [
                [
                    InlineKeyboardButton(
                        text=recent_jobs.name,
                        callback_data=register_cb.new("recentJob", recent_jobs.id, 0)
                    ),
                    InlineKeyboardButton(
                        text="❌",
                        callback_data=register_cb.new("DelrecentJob", recent_jobs.id, 0)
                    )
                ]
                for recent_jobs in recent_job
            ]
            if len(recent_job) == 3:
                keyboards.append([InlineKeyboardButton(text="Продолжить", callback_data=register_cb.new("next", 0, 0))])
            else:
                if len(recent_job) >= 1:
                    keyboards.append(
                        [InlineKeyboardButton(text="➕", callback_data=register_cb.new("addRecentJobEdit", 1, 0))] +
                        [InlineKeyboardButton(text="Продолжить", callback_data=register_cb.new("next", 0, 0))]
                    )
                else:
                    keyboards.append(
                        [
                            InlineKeyboardButton(text="➕", callback_data=register_cb.new("addRecentJobEdit", 2, 0)),
                        ] + [
                            InlineKeyboardButton(text="Продолжить", callback_data=register_cb.new("next", 3, 0))
                        ]
                    )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=keyboards
            )
            return keyboard
        else:
            keyboards = [
                [
                    InlineKeyboardButton(
                        text=recent_jobs.name,
                        callback_data=register_cb.new("recentJob", recent_jobs.id, 0)
                    )
                ]
                for recent_jobs in recent_job
            ]
            if len(recent_job) == 3:
                keyboards.append([InlineKeyboardButton(text="Продолжить", callback_data=register_cb.new("next", 0, 0))])
                keyboards.append([InlineKeyboardButton(text="Назад", callback_data=register_cb.new(targetBack, 0, 0))])
            else:
                if len(recent_job) >= 1:
                    keyboards.append(
                        [InlineKeyboardButton(text="➕", callback_data=register_cb.new("addRecentJob", 1, 0))] +
                        [InlineKeyboardButton(text="Продолжить", callback_data=register_cb.new("next", 0, 0))] +
                        [InlineKeyboardButton(text="Назад", callback_data=register_cb.new(targetBack, 0, 0))]
                    )
                else:
                    keyboards.append(
                        [
                            InlineKeyboardButton(text="➕", callback_data=register_cb.new("addRecentJob", 2, 0))
                        ] +
                        [
                            InlineKeyboardButton(text="Пропустить", callback_data=register_cb.new("next", 3, 0))
                        ]
                    )
                    keyboards.append(
                        [
                            InlineKeyboardButton(text="Назад", callback_data=register_cb.new(targetBack, 0, 0))
                        ]
                    )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=keyboards
            )
            return keyboard

    @staticmethod
    async def complete_ikb(applicant_form: int) -> InlineKeyboardMarkup:

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Завершить регистрацию",
                                         callback_data=register_cb.new("complete", applicant_form, 0)),
                    InlineKeyboardButton(text="Редактировать",
                                         callback_data=register_cb.new("editQuestionnaire", applicant_form, 0)),
                ]
            ]
        )

    @staticmethod
    async def send_contact_ikb() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            row_width=2,
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text='Поделиться контактом',
                                   request_contact=True),
                    KeyboardButton(text='Назад', callback_data=register_cb.new("editQuestionnaire", 0, 0))
                ]
            ]
        )

    @staticmethod
    async def process(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            if callback.data.startswith("reg"):
                data = register_cb.parse(callback_data=callback.data)
                # 2
                if data.get("target") == "date_of_birth":
                    id = data.get('id')
                    if int(id) == 5:
                        await state.update_data(registration=True)
                    else:
                        await state.update_data(registration=False)

                    if await CRUDUser.get(user_id=callback.from_user.id) is None:
                        await CRUDUser.add(user=UserSchema(id=callback.from_user.id, role_id=Roles.Applicant.value))

                    await UserRegister.DateOfBirth.set()
                    await callback.message.edit_text(
                        text="Заполнение анкеты\nВыберите дату рождения:",
                        reply_markup=(await DialogCalendar().start_calendar())
                    )
                # 3
                elif data.get("target") == "CitizenshipId":
                    data1 = await state.get_data()
                    await state.update_data(citizenship_id=int(data.get("id")))

                    await UserRegister.Subpositions.set()
                    await callback.message.edit_text(text="Какую работу вы ищите?",
                                                     reply_markup=await Register.position_ikb(target="Subpositions",
                                                                                              CRUD=CRUDPosition,
                                                                                              postion=True,
                                                                                              registration=data1[
                                                                                                  'registration'],
                                                                                              targetBack="backCitizenship")
                                                     )
                # 4
                elif data.get("target") == "WorkExperienceId":
                    data1 = await state.get_data()
                    await state.update_data(work_experience_id=int(data.get("id")))
                    await state.update_data(user_id=callback.from_user.id)

                    await UserRegister.KnowledgeOfEnglish.set()
                    await callback.message.edit_text(text="Знание английского языка",
                                                     reply_markup=await Register.english_ikb(
                                                         registration=data1['registration'],
                                                         targetBack="backWorkExperienceId")
                                                     )

                elif data.get("target") == "Subpositions":
                    data1 = await state.get_data()

                    position_id = data.get('id')
                    await state.update_data(subposition=data.get("id"))

                    await UserRegister.RecentJob.set()
                    await callback.message.edit_text(text='Выберите должность',
                                                     reply_markup=await Register.position_ikb(target="RecentJob",
                                                                                              CRUD=CRUDPosition,
                                                                                              subpositions_id=int(
                                                                                                  position_id),
                                                                                              registration=data1[
                                                                                                  'registration'],
                                                                                              targetBack="backCitizenship",
                                                                                              targetNext="RecentJob")
                                                     )

                # elif data.get("target") == "AddPosition":
                #     position_id = data.get('id')
                #
                #     user_data = await state.get_data()
                #     subposition_id = user_data.get('subposition')
                #
                #     user_data["work_experience_id"] = 1
                #     user_data["knowledge_of_english"] = 1
                #     user_data["position_id"] = position_id
                #     user_data["user_id"] = callback.from_user.id
                #
                #     applicant_form = await CRUDApplicantForm.add(applicant_form=ApplicantFormSchema(**user_data))
                #
                #     await callback.message.edit_text(text='Выберите еще должность',
                #                                      reply_markup=await Register.position_ikb(target="AddPosition",
                #                                                                               CRUD=CRUDPosition,
                #                                                                               subpositions_id=int(
                #                                                                                   subposition_id),
                #                                                                               registration=user_data[
                #                                                                                   'registration'],
                #                                                                               targetBack="backCitizenship",
                #                                                                               targetNext="RecentJob",
                #                                                                               user_id=callback.from_user.id)
                #                                      )


                elif data.get("target") == "RecentJob":
                    data1 = await state.get_data()
                    await state.update_data(position_id=data.get("id"))
                    # await UserRegister.WorkExperienceId.set()
                    await callback.message.edit_text(text="Выберите ваш опыт работы\n"
                                                          "на претендуемую должность",
                                                     reply_markup=await Register.work_experience_ikb(
                                                         registration=data1['registration'],
                                                         targetBack="backRecentJob")
                                                     )

                elif data.get("target") == "English":
                    data1 = await state.get_data()
                    await state.update_data(knowledge_of_english=int(data.get("id")))

                    await UserRegister.InstagramUrl.set()
                    await callback.message.edit_text(text='Введите <b>Имя пользователя</b> instagram',
                                                     reply_markup=await Register.skip_ikb(target="Instagram",
                                                                                          registration=data1[
                                                                                              'registration'],
                                                                                          targetBack="backEnglish"),
                                                     parse_mode="HTML")

                elif data.get("target") == "Instagram":
                    data = await state.get_data()
                    await callback.message.delete()
                    await UserRegister.PhoneNumber.set()

                    await callback.message.answer(text="Введите номер телефона\n"
                                                       "или поделитесь своим контактом",
                                                  reply_markup=await Register.send_contact(
                                                      registration=data['registration'],
                                                      targetBack="backFIO"))

                # 4
                elif data.get("target") == "addRecentJob":
                    await UserRegister.NewRecentJob.set()
                    await callback.message.edit_text(
                        text="Введите ваше последнее место работы",
                    )
                # elif data.get("target") == "Patronymic":
                #     data = await state.get_data()
                #     await UserRegister.isMarried.set()
                #     await callback.message.edit_text(text='Семейное положение\n'
                #                                           'Замужем, женаты?',
                #                                      reply_markup=await Register.approve_ikb(target="isMarried",
                #                                                                              registration=data[
                #                                                                                  'registration'])
                #                                      )

                # elif data.get("target") == "city":
                #     city_id = int(data.get("id"))
                #     data = await state.get_data()
                #     await state.update_data(city_id=city_id)
                #     await UserRegister.Name.set()
                #     if data['registration']:
                #         await callback.message.edit_text(
                #             text="Введите имя:"
                #         )
                #     else:
                #         await callback.message.edit_text(
                #             text="Введите имя:", reply_markup=await Register.cancel_ikb()
                #         )
                # elif data.get("target") == "isMarried":
                #     is_married: bool = True if int(data.get("id")) == Option.is_true.value else False
                #     data = await state.get_data()
                #
                #     await callback.message.delete()
                #     await state.update_data(is_married=is_married)
                #     await UserRegister.PhoneNumber.set()
                #     await callback.message.answer(
                #         text='Номер телефона',
                #         reply_markup=await Register.send_contact(registration=data['registration'])
                #     )

                elif data.get("target") == "backWorkExperienceId":
                    data1 = await state.get_data()
                    await callback.message.edit_text(text="Выберите ваш опыт работы\n"
                                                          "на претендуемую должность",
                                                     reply_markup=await Register.work_experience_ikb(
                                                         registration=data1['registration'],
                                                         targetBack="backCitizenship")
                                                     )

                elif data.get("target") == "backPhone":
                    await callback.message.delete()
                    await UserRegister.PhoneNumber.set()
                    await callback.message.answer(text="Введите номер телефона\n"
                                                       "или поделитесь своим контактом",
                                                  reply_markup=await Register.send_contact(targetBack="Instagram"))

                elif data.get("target") == "backInstagram":
                    data = await state.get_data()
                    await UserRegister.InstagramUrl.set()
                    await callback.message.edit_text(text='Введите <b>Имя пользователя</b> instagram',
                                                     reply_markup=await Register.skip_ikb(target="WorkExperienceId",
                                                                                          registration=data[
                                                                                              'registration'],
                                                                                          targetBack="WorkExperienceId"),
                                                     parse_mode="HTML")

                elif data.get("target") == "backFIO":
                    await UserRegister.FIO.set()
                    await callback.message.edit_text(
                        text="Как нам вас представить?\n"
                             "Введите ФИО:", reply_markup=await Register.cancel_ikb(target="date_of_birth")
                    )

                elif data.get("target") == "backCitizenship":

                    await callback.message.edit_text(text='Выберите гражданство',
                                                     reply_markup=await Register.position_ikb(
                                                         target="CitizenshipId",
                                                         CRUD=CRUDCitizenShip,
                                                         targetBack="backFIO")
                                                     )

                elif data.get("target") == "backEnglish":
                    data1 = await state.get_data()
                    await UserRegister.KnowledgeOfEnglish.set()
                    await callback.message.edit_text(text="Знание английского языка",
                                                     reply_markup=await Register.english_ikb(
                                                         registration=data1['registration'],
                                                         targetBack="RecentJob")
                                                     )

                elif data.get("target") == "backRecentJob":
                    data1 = await state.get_data()
                    await callback.message.edit_text(text="Какую работу вы ищите?",
                                                     reply_markup=await Register.position_ikb(target="Subpositions",
                                                                                              CRUD=CRUDPosition,
                                                                                              postion=True,
                                                                                              registration=data1[
                                                                                                  'registration'],
                                                                                              targetBack="backCitizenship")
                                                     )

                elif data.get("target") == "next":
                    data = await state.get_data()

                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data.get("applicant_form")))
                    citizenship = await CRUDCitizenShip.get(citizenship_id=applicant_form.citizenship_id)
                    work_experience = await CRUDWorkExperience.get(work_experience_id=applicant_form.work_experience_id)
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
                        phone = applicant_form.phone_number

                    if applicant_form.instagram_url is None:
                        insta: str = 'N/A'
                    else:
                        insta = applicant_form.instagram_url

                    date_date_of_birth: str = str(applicant_form.date_of_birth.day) + "." \
                                              + str(applicant_form.date_of_birth.month) + "." \
                                              + str(applicant_form.date_of_birth.year)

                    recent_job_user = ' '
                    count = 0
                    data_count = ["①", "➁", "③"]
                    get_recent_job = await CRUDRecentJob.get_name(recent_job_id=applicant_form.id)  # переделать
                    if get_recent_job:
                        for i in get_recent_job:
                            recent_job_user += f"\n{data_count[count]} - Профессия: {i.name}\n"
                            count += 1
                    else:
                        recent_job_user = "N/A"

                    text = f"<b>Фамилия</b>: {applicant_form.surname}\n" \
                           f"<b>Имя:</b>  {applicant_form.name}\n" \
                           f"<b>Отчество:</b>  {patronymic}\n" \
                           f"📅 <b>Дата рождения:</b>  {date_date_of_birth}\n" \
                           f"👥 <b>Гражданство:</b> {citizenship.name}\n" \
                           f"📱 <b>Телефон:</b>  <code>{phone}</code>\n" \
                           f"🇺🇸 <b>Английский:</b> {knowledge_of_english.name}\n" \
                           f"🗂 <b>Желаемая должность:</b> {position.name}\n" \
                           f"💪 <b>Опыт работы" \
                           f"на претендуемую должность: </b>  {work_experience.name}\n"\
                           f"📷 <b>Instagram</b> : <a href='www.instagram.com/{insta}/'>{insta}</a>\n\n" \
                           f"👨🏻‍💻 <b>Последнее место работы:</b> {recent_job_user}\n" \


                    await callback.message.edit_text(
                        text="Проверьте правильность данных и подтвердите!\n\n" + text,
                        reply_markup=await Register.complete_ikb(applicant_form=int(data.get("applicant_form")))
                    )

                elif data.get("target") == "complete":
                    await state.finish()
                    await callback.message.edit_text(text='Главное меню\nУспешно зарегистрировались!',
                                                     reply_markup=await Register.profile_ikb(callback.from_user.id,
                                                                                             registration=False))

                elif data.get("target") == "cancellation":
                    if await CRUDRecentJob.get(applicant_form_id=int(data.get("id"))):
                        await CRUDRecentJob.delete(applicant_form_id=int(data.get("id")))

                    await CRUDApplicantForm.delete(applicant_form_id=int(data.get("id")))
                    await callback.message.edit_text(text='Отмена',
                                                     reply_markup=await Register.profile_ikb(callback.from_user.id,
                                                                                             registration=False))
                    await state.finish()

                elif data.get("target") == "editQuestionnaire":
                    data = await state.get_data()
                    await callback.message.edit_text(text="Редактировать",
                                                     reply_markup=await Register.editQuestionnaire_ikb(data))

                elif data.get('target') == 'canceled':
                    await state.finish()
                    await callback.message.edit_text(
                        text="ГЛАВНОЕ МЕНЮ",
                        reply_markup=await Register.profile_ikb(user_id=callback.from_user.id, registration=False)
                    )

                elif data.get('target') == "Edit":
                    edit_id = int(data.get('id'))
                    # Фамилия+
                    if edit_id == 0:
                        await EditRegister.Surname.set()
                        await callback.message.edit_text(text="Введите фамилию",
                                                         reply_markup=await Register.back())

                    # Имя+
                    elif edit_id == 1:
                        await EditRegister.Name.set()
                        await callback.message.edit_text(text="Введите имя",
                                                         reply_markup=await Register.back())

                    # Отчество+
                    elif edit_id == 2:
                        await EditRegister.Patronymic.set()
                        await callback.message.edit_text(text="Введите отчество",
                                                         reply_markup=await Register.back())

                    # Дата рождения
                    elif edit_id == 3:
                        pass

                    # Гражданство+
                    elif edit_id == 4:
                        await callback.message.edit_text(text='Выберите гражданство',
                                                         reply_markup=await Register.position_ikb(
                                                             target="CitizenshipEdit",
                                                             CRUD=CRUDCitizenShip,
                                                             edit=True)
                                                         )

                    # Номер телефона+
                    elif edit_id == 5:
                        await callback.message.delete()
                        await EditRegister.PhoneNumber.set()
                        await callback.message.answer(text="Введите номер телефона\n"
                                                           "или поделитесь своим контактом",
                                                      reply_markup=await Register.send_contact_ikb())

                    # Инстаграм+
                    elif edit_id == 6:
                        await EditRegister.InstagramUrl.set()
                        await callback.message.edit_text(text="Введите Имя пользователя Instagram",
                                                         reply_markup=await Register.back())

                    # Английский+
                    elif edit_id == 7:
                        await callback.message.edit_text(text="Уровень английского",
                                                         reply_markup=await Register.english_ikb(target="EnglishEdit",
                                                                                                 edit=True))

                    # Стаж+
                    elif edit_id == 8:
                        await callback.message.edit_text(text="Выберите ваш опыт работы",
                                                         reply_markup=await Register.work_experience_ikb(edit=True)
                                                         )

                    # Желаемое место работы+
                    elif edit_id == 9:
                        data_edit = await state.get_data()
                        user = await CRUDApplicantForm.get(applicant_form_id=int(data_edit.get("applicant_form")))
                        position = await CRUDPosition.get(position_id=user.position_id)
                        text = f"Желаемое место работы : <i>{position.name}</i>\n\n" \
                               f"Выберите новое желаемое место работы"
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await Register.position_ikb(
                                                             target="SubpositionsEdit",
                                                             CRUD=CRUDPosition,
                                                             position_edit=True,
                                                         ))

                    # Последние места работы
                    elif edit_id == 10:
                        data_edit = await state.get_data()
                        await state.update_data(applicant_form_id=int(data_edit.get("applicant_form")))
                        await callback.message.edit_text(text="Последние места работы",
                                                         reply_markup=await Register.recent_job_ikb(
                                                             recent_job_id=int(data_edit.get("applicant_form")),
                                                             edit=True)
                                                         )

                elif data.get("target") == "CitizenshipEdit":
                    current_id = int(data.get("id"))
                    data_edit = await state.get_data()
                    data_edit["citizenship_id"] = current_id
                    await state.update_data(citizenship_id=current_id)
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data_edit.get("applicant_form")))
                    citizenship_id = current_id
                    applicant_form.citizenship_id = int(citizenship_id)

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Гражданство изменено",
                                                     reply_markup=await Register.editQuestionnaire_ikb(data=data_edit))

                elif data.get("target") == "EnglishEdit":
                    current_id = int(data.get("id"))
                    data_edit = await state.get_data()
                    data_edit["knowledge_of_english"] = current_id
                    await state.update_data(knowledge_of_english=current_id)
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data_edit.get("applicant_form")))
                    knowledge_of_english = current_id
                    applicant_form.knowledge_of_english = int(knowledge_of_english)

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Английский изменен",
                                                     reply_markup=await Register.editQuestionnaire_ikb(data=data_edit))

                elif data.get("target") == "WorkExperienceEdit":
                    current_id = int(data.get("id"))
                    data_edit = await state.get_data()
                    data_edit["work_experience_id"] = current_id
                    await state.update_data(work_experience_id=current_id)
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data_edit.get("applicant_form")))
                    work_experience = current_id
                    applicant_form.work_experience_id = int(work_experience)

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Опыт работы изменен",
                                                     reply_markup=await Register.editQuestionnaire_ikb(data=data_edit))

                elif data.get("target") == "SubpositionsEdit":
                    current_id = int(data.get("id"))
                    data_edit = await state.get_data()

                    await state.update_data(work_experience_id=current_id)
                    user = await CRUDApplicantForm.get(applicant_form_id=int(data_edit.get("applicant_form")))
                    position = await CRUDPosition.get(position_id=user.position_id)
                    text = f"Желаемое место работы : <i>{position.name}</i>\n\n" \
                           f"Выберите новое желаемое место работы"

                    await callback.message.edit_text(text=text,
                                                     reply_markup=await Register.position_ikb(target="PositionEdit",
                                                                                              CRUD=CRUDPosition,
                                                                                              subpositions_edit_id=current_id))

                elif data.get("target") == "PositionEdit":
                    current_id = int(data.get("id"))
                    data_edit = await state.get_data()
                    data_edit["position_id"] = current_id
                    await state.update_data(position_id=current_id)
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data_edit.get("applicant_form")))
                    position = current_id
                    applicant_form.position_id = int(position)

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await callback.message.edit_text(text="Должность изменена",
                                                     reply_markup=await Register.editQuestionnaire_ikb(data=data_edit))

                elif data.get("target") == "addRecentJobEdit":
                    await EditRegister.NewRecentJob.set()
                    await callback.message.edit_text(
                        text="Введите ваше последнее место работы",
                    )

                elif data.get("target") == "DelrecentJob":
                    current_user_id = int(data.get("id"))
                    data_edit = await state.get_data()
                    await CRUDRecentJob.delete(recent_job_id=current_user_id)
                    await callback.message.edit_text(text="Место работы <b>удалено</b>",
                                                     reply_markup=await Register.recent_job_ikb(
                                                         recent_job_id=int(data_edit["applicant_form"]),
                                                         edit=True)
                                                     )

            elif callback.data.startswith("dialog_calendar"):
                data = calendar_callback.parse(callback_data=callback.data)
                date_of_birth = datetime(year=int(data.get("year")), day=int(data.get("day")),
                                         month=int(data.get("month")))
                await state.update_data(date_of_birth=date_of_birth)

                await UserRegister.FIO.set()
                await callback.message.edit_text(
                    text="Как нам вас представить?\n"
                         "Введите ФИО:", reply_markup=await Register.cancel_ikb(target="date_of_birth")
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
                if await state.get_state() == "UserRegister:FIO":
                    data = message.text.split()
                    if len(data) == 3:
                        await state.update_data(surname=data[0])
                        await state.update_data(name=data[1])
                        await state.update_data(patronymic=data[2])

                        await message.answer(text='Выберите гражданство',
                                             reply_markup=await Register.position_ikb(
                                                 target="CitizenshipId",
                                                 CRUD=CRUDCitizenShip,
                                                 targetBack="backFIO")
                                             )

                        await UserRegister.CitizenshipId.set()

                    elif len(data) == 2:
                        await state.update_data(name=data[0])
                        await state.update_data(surname=data[1])
                        await state.update_data(patronymic="N/A")

                        await UserRegister.CitizenshipId.set()
                        await message.answer(text='Выберите гражданство',
                                             reply_markup=await Register.position_ikb(
                                                 target="CitizenshipId",
                                                 CRUD=CRUDCitizenShip,
                                                 targetBack="backFIO")
                                             )

                    else:
                        await UserRegister.FIO.set()
                        await message.answer(text="ФИО введено не верно\n"
                                                  "Через пробел введите Фамилию, Имя, Отчество ",
                                             reply_markup=await Register.cancel_ikb(target="date_of_birth"))

                elif await state.get_state() == "UserRegister:PhoneNumber":
                    if message.content_type == "contact":
                        examination_phone = "+" + message.contact.phone_number
                        if examination_phone[1] == "7":
                            await state.update_data(phone_number="+"+message.contact.phone_number)
                            user_data = await state.get_data()
                            applicant_form = await CRUDApplicantForm.add(
                                applicant_form=ApplicantFormSchema(**user_data))

                            await state.update_data(applicant_form=applicant_form.id)

                            await UserRegister.AddRecentJob.set()
                            await message.answer(text="Ваши последние места работы",
                                                 reply_markup=await Register.recent_job_ikb(
                                                     recent_job_id=applicant_form.id,
                                                     targetBack="backPhone")
                                                 )
                        else:
                            await UserRegister.PhoneNumber.set()
                            await message.answer(
                                text='Вы ввели не верный формат телефона\n'
                                     'Пример (+7 000 000 00 00) без пробелов',
                                reply_markup=await Register.send_contact(targetBack="WorkExperienceId")
                            )
                    elif message.text == "Пропустить":

                        user_data = await state.get_data()
                        try:
                            applicant_form = await CRUDApplicantForm.add(applicant_form=ApplicantFormSchema(**user_data))
                        except ValidationError:
                            applicant_form = await CRUDApplicantForm.add(applicant_form=ApplicantFormSchema(**user_data))

                        await state.update_data(applicant_form=applicant_form.id)
                        await UserRegister.AddRecentJob.set()
                        await message.answer(text="Ваши последние места работы",
                                             reply_markup=await Register.recent_job_ikb(
                                                 recent_job_id=applicant_form.id,
                                                 targetBack="backPhone")
                                             )
                    elif message.text == "Назад":
                        await UserRegister.InstagramUrl.set()
                        await message.answer(text='Инстаграм',
                                             reply_markup=await Register.skip_ikb(target="Instagram",
                                                                                  targetBack="WorkExperienceId"))
                    else:
                        examination_phone = message.text
                        edit_examination_phone = message.text.lstrip("+")
                        digit_phone = edit_examination_phone.isdigit()
                        if len(message.text) != 12 or not digit_phone:

                            await UserRegister.PhoneNumber.set()
                            await message.answer(
                                text='Вы ввели не верный формат телефона\n'
                                     'Пример (+7 000 000 00 00) без пробелов',
                                reply_markup=await Register.send_contact(targetBack="WorkExperienceId")
                            )
                        else:
                            if examination_phone[1] == "7":
                                await state.update_data(phone_number=message.text)
                                if message.text == "Отмена":
                                    await state.finish()
                                    await message.answer(
                                        text="ГЛАВНОЕ МЕНЮ",
                                        reply_markup=await Register.profile_ikb(user_id=message.from_user.id,
                                                                                registration=False)
                                    )
                                else:
                                    await state.update_data(phone_number=message.text)
                                    user_data = await state.get_data()
                                    applicant_form = await CRUDApplicantForm.add(
                                        applicant_form=ApplicantFormSchema(**user_data))

                                    await state.update_data(applicant_form=applicant_form.id)

                                    await UserRegister.AddRecentJob.set()
                                    await message.answer(text="Ваши последние места работы",
                                                         reply_markup=await Register.recent_job_ikb(
                                                             recent_job_id=applicant_form.id,
                                                             targetBack="backPhone")
                                                         )
                            else:
                                await UserRegister.PhoneNumber.set()
                                await message.answer(
                                    text='Вы ввели не верный формат телефона\n'
                                         'Пример (+7 000 000 00 00) без пробелов',
                                    reply_markup=await Register.send_contact(targetBack="WorkExperienceId")
                                )

                elif await state.get_state() == "UserRegister:InstagramUrl":
                    data = await state.get_data()
                    await state.update_data(instagram_url=message.text)
                    await UserRegister.PhoneNumber.set()
                    await message.answer(text="Введите номер телефона\n"
                                              "или поделитесь своим контактом",
                                         reply_markup=await Register.send_contact(targetBack="Instagram"))

                elif await state.get_state() == "UserRegister:NewRecentJob":

                    await state.update_data(recent_job=message.text)
                    data_user = await state.get_data()
                    await CRUDRecentJob.add(
                        recent_job=RecentJobSchema(name=data_user['recent_job'],
                                                   applicant_form_id=int(data_user['applicant_form'])))
                    await message.answer(
                        text=f"{data_user['recent_job']} добавлен в ваш список!",
                        reply_markup=await Register.recent_job_ikb(int(data_user['applicant_form']),
                                                                   targetBack="backPhone")
                    )

                elif await state.get_state() == "EditRegister:Surname":
                    data = await state.get_data()
                    data["surname"] = message.text
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form"]))
                    applicant_form.surname = message.text
                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await message.answer(text="Фамилия изменена",
                                         reply_markup=await Register.editQuestionnaire_ikb(data=data))
                elif await state.get_state() == "EditRegister:Name":
                    data = await state.get_data()
                    data["name"] = message.text
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form"]))
                    applicant_form.name = message.text
                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await message.answer(text="Имя изменено",
                                         reply_markup=await Register.editQuestionnaire_ikb(data=data))
                elif await state.get_state() == "EditRegister:Patronymic":
                    data = await state.get_data()
                    data["patronymic"] = message.text
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form"]))
                    applicant_form.patronymic = message.text
                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await message.answer(text="Имя изменено",
                                         reply_markup=await Register.editQuestionnaire_ikb(data=data))
                elif await state.get_state() == "EditRegister:InstagramUrl":
                    data = await state.get_data()
                    data["instagram_url"] = message.text
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form"]))
                    applicant_form.instagram_url = message.text
                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await message.answer(text="Instagram изменен",
                                         reply_markup=await Register.editQuestionnaire_ikb(data=data))
                elif await state.get_state() == "EditRegister:PhoneNumber":
                    data = await state.get_data()
                    applicant_form = await CRUDApplicantForm.get(applicant_form_id=int(data["applicant_form"]))
                    if message.content_type == "contact":
                        applicant_form.phone_number = message.contact.phone_number
                        data["phone_number"] = message.contact.phone_number
                    elif message.text == "Назад":
                        applicant_form.phone_number = "N/A"
                        data["phone_number"] = message.text
                    else:
                        applicant_form.phone_number = message.text
                        data["phone_number"] = message.text

                    await CRUDApplicantForm.update(applicant_form=applicant_form)
                    await message.answer(text="Телефон изменен",
                                         reply_markup=await Register.editQuestionnaire_ikb(data=data))
                elif await state.get_state() == "EditRegister:NewRecentJob":
                    await state.update_data(recent_job=message.text)
                    data_user = await state.get_data()
                    await CRUDRecentJob.add(
                        recent_job=RecentJobSchema(name=data_user['recent_job'],
                                                   applicant_form_id=int(data_user['applicant_form'])))
                    await message.answer(
                        text=f"{data_user['recent_job']} добавлен в ваш список!",
                        reply_markup=await Register.recent_job_ikb(int(data_user['applicant_form']), edit=True)
                    )
                # if await state.get_state() == "UserRegister:Name":
                #     data = await state.get_data()
                #     await state.update_data(name=message.text.strip().title())
                #     await UserRegister.Surname.set()
                #
                #     if data['registration']:
                #         await message.answer(
                #             text="Введите фамилию:"
                #         )
                #     else:
                #         await message.answer(
                #             text="Введите фамилию:", reply_markup=await Register.cancel_ikb()
                #         )
                # elif await state.get_state() == "UserRegister:Surname":
                #     data = await state.get_data()
                #     await state.update_data(surname=message.text.strip().title())
                #     await UserRegister.Patronymic.set()
                #     await message.answer(
                #         text="Введите отчество:",
                #         reply_markup=await Register.skip_ikb(target="Patronymic", registration=data['registration'])
                #     )
                # elif await state.get_state() == "UserRegister:Patronymic":
                #     data = await state.get_data()
                #     await state.update_data(patronymic=message.text.strip().title())
                #
                #     await UserRegister.isMarried.set()
                #     await message.answer('Семейное положение\n'
                #                          'Замужем, женаты?', reply_markup=await Register.approve_ikb(target="isMarried",
                #                                                                                      registration=data[
                #                                                                                          'registration'])
                #                          )
