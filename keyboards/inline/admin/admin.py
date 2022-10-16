from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest
from crud import CRUDUser, CRUDVacancy, CRUDApplicantForm, CRUDAge
from crud.citizenship import CRUDCitizenShip
from crud.city import CRUDCity
from crud.position import CRUDPosition
from crud.work_experiences import CRUDWorkExperience
from keyboards.inline.admin.age import list_ages_ikb
from keyboards.inline.admin.citizenship import list_all_citizenships_ikb
from keyboards.inline.admin.city import list_cities_ikb
from keyboards.inline.admin.position import list_positions_ikb, list_subpositions_ikb
from keyboards.inline.admin.work_experience import list_all_work_experience_ikb
from loader import bot
from schemas import CitySchema, CitizenShipSchema, PositionSchema, WorkExperienceSchema, AgeSchema
from states.admins import AddCityFSM, AddCitizenshipFSM, AddPositionFSM, AddSubPositionFSM, AddWorkExperienceFSM, \
    AddMailingFSM, AddAgeFSM

admin_cb = CallbackData("admin", "action", "target", "id")


async def admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Города",
                    callback_data=admin_cb.new("get_all", "cities", 0)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Гражданства",
                    callback_data=admin_cb.new("get_all", "citizenships", 0)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Должности",
                    callback_data=admin_cb.new("get_all", "positions", 0)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Опыт работы",
                    callback_data=admin_cb.new("get_all", "work_experience", 0)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Возраст",
                    callback_data=admin_cb.new("get_all", "ages", 0)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Рассылка",
                    callback_data=admin_cb.new("get_all", "mailing", 0)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Статистика",
                    callback_data=admin_cb.new("get_all", "statistic", 0)
                )
            ],

        ]
    )
    return keyboard


async def approve(target: str, object_id: int = 0) -> InlineKeyboardMarkup:
    keyboards = [
        [
            InlineKeyboardButton(text="ДА", callback_data=admin_cb.new("approve", target, object_id)),
            InlineKeyboardButton(text="НЕТ", callback_data=admin_cb.new("incorrect", target, object_id))
        ]
    ]
    if object_id == 0:
        keyboards.append(
            [
                InlineKeyboardButton(text="ОТМЕНИТЬ", callback_data=admin_cb.new("revoke", target, object_id))
            ]
        )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def back_ikb() -> InlineKeyboardMarkup:
    keyboards = [
        [
            InlineKeyboardButton(text="Назад", callback_data=admin_cb.new("back", "back_admin_menu", 0))
        ]
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def mailing_type_ikb() -> InlineKeyboardMarkup:
    keyboards = [
        [
            InlineKeyboardButton(text="Текстовая",
                                 callback_data=admin_cb.new("text_mailing", "mailing", 0)),
            InlineKeyboardButton(text="Текстовая + картинка",
                                 callback_data=admin_cb.new("text_and_photo_mailing", "mailing", 0))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data=admin_cb.new("back", "back_admin_menu", 0))
        ]
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


class AdminPanel:

    @staticmethod
    async def start() -> InlineKeyboardMarkup:
        return await admin_menu()

    @staticmethod
    async def process(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            data = admin_cb.parse(callback_data=callback.data)
            # Апрувы
            if state:
                if data.get("action") == "revoke":
                    if data.get("target") == "subpositions":
                        state_data: dict = await state.get_data()
                        position_id = state_data.get('position_id')
                        data["id"] = position_id
                    await state.finish()
                    await callback.answer(
                        text=f"Добавление было отменено!"
                    )
                    data["action"] = "get_all"

                if await state.get_state() == "AddCityFSM:Approve":
                    if data.get("action") == "approve":
                        state_data: dict = await state.get_data()
                        name = state_data.get('city')
                        await CRUDCity.add(city=CitySchema(name=name))
                        await state.finish()
                        await callback.answer(
                            text=f"Город {name} был добавлен!"
                        )
                        await callback.message.edit_text(
                            text="<b>Города:</b>",
                            reply_markup=await list_cities_ikb()
                        )
                    elif data.get("action") == "incorrect":
                        await AddCityFSM.AddCity.set()
                        await callback.answer(
                            text=f"Попробуйте еще раз!"
                        )
                        await callback.message.edit_text(
                            text="<b>Введите название города:</b>"
                        )
                elif await state.get_state() == "AddCitizenshipFSM:Approve":
                    if data.get("action") == "approve":
                        state_data: dict = await state.get_data()
                        name = state_data.get('citizenship')
                        await CRUDCitizenShip.add(citizen_ship=CitizenShipSchema(name=name))
                        await state.finish()
                        await callback.answer(
                            text=f"Гражданство {name} было добавлено!"
                        )
                        await callback.message.edit_text(
                            text="<b>Гражданства:</b>",
                            reply_markup=await list_all_citizenships_ikb()
                        )
                    elif data.get("action") == "incorrect":
                        await AddCitizenshipFSM.AddCitizenship.set()
                        await callback.answer(
                            text=f"Попробуйте еще раз!"
                        )
                        await callback.message.edit_text(
                            text="<b>Введите гражданство, которое хотите добавить:</b>"
                        )
                elif await state.get_state() == "AddPositionFSM:Approve":
                    if data.get("action") == "approve":
                        state_data: dict = await state.get_data()
                        name = state_data.get('position')
                        await CRUDPosition.add(position=PositionSchema(name=name))
                        await state.finish()
                        await callback.answer(
                            text=f"Должность {name} была добавлена!"
                        )
                        await callback.message.edit_text(
                            text="<b>Должности:</b>",
                            reply_markup=await list_positions_ikb()
                        )
                    elif data.get("action") == "incorrect":
                        await AddPositionFSM.AddPosition.set()
                        await callback.answer(
                            text=f"Попробуйте еще раз!"
                        )
                        await callback.message.edit_text(
                            text="<b>Введите должность, которую хотите добавить:</b>"
                        )
                elif await state.get_state() == "AddSubPositionFSM:Approve":
                    if data.get("action") == "approve":
                        state_data: dict = await state.get_data()
                        position_id = state_data.get('position_id')
                        subposition_name = state_data.get('subposition_name')
                        position = await CRUDPosition.get(position_id=position_id)
                        await CRUDPosition.add(position=PositionSchema(parent_id=position_id,
                                                                       name=subposition_name))
                        await state.finish()
                        await callback.answer(
                            text=f"Подкатегория {subposition_name} для должности {position.name} была добавлена!"
                        )
                        await callback.message.edit_text(
                            text=f"Подкатегории для должности <b>{position.name}</b>:",
                            reply_markup=await list_subpositions_ikb(position_id)
                        )
                    elif data.get("action") == "incorrect":
                        await AddSubPositionFSM.AddSubPosition.set()
                        await callback.answer(
                            text=f"Попробуйте еще раз!"
                        )
                        await callback.message.edit_text(
                            text="<b>Введите должность, которую хотите добавить:</b>"
                        )
                elif await state.get_state() == "AddWorkExperienceFSM:Approve":
                    if data.get("action") == "approve":
                        state_data: dict = await state.get_data()
                        name = state_data.get('work_experience')
                        await CRUDWorkExperience.add(work_experience=WorkExperienceSchema(name=name))
                        await state.finish()
                        await callback.answer(
                            text=f"Вариант опыта работы {name} был добавлен!"
                        )
                        await callback.message.edit_text(
                            text="<b>Опыт работы:</b>",
                            reply_markup=await list_all_work_experience_ikb()
                        )
                    elif data.get("action") == "incorrect":
                        await AddWorkExperienceFSM.AddWorkExperience.set()
                        await callback.answer(
                            text=f"Попробуйте еще раз!"
                        )
                        await callback.message.edit_text(
                            text="<b>Введите вариант опыта работы:</b>"
                        )
                elif await state.get_state() == "AddAgeFSM:Approve":
                    if data.get("action") == "approve":
                        state_data: dict = await state.get_data()
                        age = state_data.get('age')
                        await CRUDAge.add(age=AgeSchema(name=age))
                        await state.finish()
                        await callback.answer(
                            text=f"Вариант возраста {age} был добавлен!"
                        )
                        await callback.message.edit_text(
                            text="<b>Возраст:</b>",
                            reply_markup=await list_ages_ikb()
                        )
                    elif data.get("action") == "incorrect":
                        await AddAgeFSM.AddAge.set()
                        await callback.answer(
                            text=f"Попробуйте еще раз!"
                        )
                        await callback.message.edit_text(
                            text="<b>Введите вариант возраста:</b>"
                        )
                elif await state.get_state() == "AddMailingFSM:Approve":
                    if data.get("action") == "approve":
                        state_data: dict = await state.get_data()
                        text = state_data.get('text')
                        await state.finish()
                        if state_data.get('photo_id'):
                            users = await CRUDUser.get_all()
                            for user in users:
                                await bot.send_photo(
                                    chat_id=user.id,
                                    photo=state_data.get('photo_id'),
                                    caption=text,
                                    parse_mode="HTML"
                                )
                        else:
                            users = await CRUDUser.get_all()
                            for user in users:
                                await bot.send_message(
                                    chat_id=user.id,
                                    text=text,
                                    parse_mode="HTML"
                                )
                        await callback.answer(
                            text=f"Рассылка произведена!"
                        )
                        await callback.message.delete()
                        await callback.message.answer(
                            text="Выберите тип рассылки:",
                            reply_markup=await mailing_type_ikb()
                        )
                    elif data.get("action") == "incorrect":
                        await AddMailingFSM.AddText.set()
                        await callback.answer(
                            text=f"Попробуйте еще раз!"
                        )
                        await callback.message.delete()
                        await callback.message.answer(
                            text="<b>Введите текст заново:</b>"
                        )
            # Кнопка назад
            if data.get("action") == "back":
                if data.get("target") == "back_admin_menu":
                    await callback.message.edit_text(
                        text="<b>Админ панель!</b>",
                        reply_markup=await AdminPanel.start()
                    )
                elif data.get("target") == "back_cities":
                    await callback.message.edit_text(
                        text="<b>Города:</b>",
                        reply_markup=await list_cities_ikb()
                    )
                elif data.get("target") == "back_citizenships":
                    await callback.message.edit_text(
                        text="<b>Гражданства:</b>",
                        reply_markup=await list_all_citizenships_ikb()
                    )
                elif data.get("target") == "back_positions":
                    await callback.message.edit_text(
                        text="<b>Должности:</b>",
                        reply_markup=await list_positions_ikb()
                    )
                elif data.get("target") == "back_subpositions":
                    position_id = int(data.get("id"))
                    position = await CRUDPosition.get(position_id=position_id)
                    await callback.message.edit_text(
                        text=f"Подкатегории для должности <b>{position.name}</b>:",
                        reply_markup=await list_subpositions_ikb(position_id)
                    )
                elif data.get("target") == "back_work_experience":
                    await callback.message.edit_text(
                        text="<b>Опыт работы:</b>",
                        reply_markup=await list_all_work_experience_ikb()
                    )
            # Города
            elif data.get("target") == "cities":
                if data.get("action") == "get_all":
                    await callback.message.edit_text(
                        text="<b>Города:</b>",
                        reply_markup=await list_cities_ikb()
                    )
                elif data.get("action") == "add":
                    await AddCityFSM.AddCity.set()
                    await callback.message.edit_text(
                        text="<b>Введите название города:</b>"
                    )
                elif data.get("action") == "del":
                    city_id = int(data.get("id"))
                    city = await CRUDCity.get(city_id=city_id)
                    await callback.message.edit_text(
                        text=f"Вы действительно хотите удалить город <b>{city.name}</b>?",
                        reply_markup=await approve(target="cities", object_id=city_id)
                    )
                elif data.get("action") == "approve":
                    city_id = int(data.get("id"))
                    if city_id:
                        city = await CRUDCity.get(city_id=city_id)
                        await CRUDCity.delete(city_id=city_id)
                        await callback.answer(
                            text=f"Город {city.name} был удален!"
                        )
                        await callback.message.edit_text(
                            text="<b>Города:</b>",
                            reply_markup=await list_cities_ikb()
                        )
                elif data.get("action") == "incorrect":
                    city_id = int(data.get("id"))
                    if city_id:
                        city = await CRUDCity.get(city_id=city_id)
                        await callback.answer(
                            text=f"Удаление города {city.name} было отменено!"
                        )
                        await callback.message.edit_text(
                            text="<b>Города:</b>",
                            reply_markup=await list_cities_ikb()
                        )
            # Гражданства
            elif data.get("target") == "citizenships":
                if data.get("action") == "get_all":
                    await callback.message.edit_text(
                        text="<b>Гражданства:</b>",
                        reply_markup=await list_all_citizenships_ikb()
                    )
                elif data.get("action") == "add":
                    await state.update_data(callback_data="citizenships")
                    await AddCitizenshipFSM.AddCitizenship.set()
                    await callback.message.edit_text(
                        text="<b>Введите гражданство, которое хотите добавить:</b>"
                    )
                elif data.get("action") == "del":
                    citizenship_id = int(data.get("id"))
                    citizenship = await CRUDCitizenShip.get(citizenship_id=citizenship_id)
                    await callback.message.edit_text(
                        text=f"Вы действительно хотите удалить гражданство <b>{citizenship.name}</b>?",
                        reply_markup=await approve(target="citizenships", object_id=citizenship_id)
                    )
                elif data.get("action") == "approve":
                    citizenship_id = int(data.get("id"))
                    if citizenship_id:
                        citizenship = await CRUDCitizenShip.get(citizenship_id=citizenship_id)
                        await CRUDCitizenShip.delete(citizenship_id=citizenship_id)
                        await callback.answer(
                            text=f"Гражданство {citizenship.name} было удалено!"
                        )
                        await callback.message.edit_text(
                            text="<b>Гражданства:</b>",
                            reply_markup=await list_all_citizenships_ikb()
                        )
                elif data.get("action") == "incorrect":
                    citizenship_id = int(data.get("id"))
                    if citizenship_id:
                        citizenship = await CRUDCitizenShip.get(citizenship_id=citizenship_id)
                        await callback.answer(
                            text=f"Удаление гражданства {citizenship.name} было отменено!"
                        )
                        await callback.message.edit_text(
                            text="<b>Гражданства:</b>",
                            reply_markup=await list_all_citizenships_ikb()
                        )
            # Должности
            elif data.get("target") == "positions":
                if data.get("action") == "get_all":
                    await callback.message.edit_text(
                        text="<b>Должности:</b>",
                        reply_markup=await list_positions_ikb()
                    )
                elif data.get("action") == "add":
                    await AddPositionFSM.AddPosition.set()
                    await callback.message.edit_text(
                        text="<b>Введите должность, которую хотите добавить:</b>"
                    )
                elif data.get("action") == "del":
                    position_id = int(data.get("id"))
                    position = await CRUDPosition.get(position_id=position_id)
                    await callback.message.edit_text(
                        text=f"Вы действительно хотите удалить должность <b>{position.name}</b> и все её подкатегории?",
                        reply_markup=await approve(target="positions", object_id=position_id)
                    )
                elif data.get("action") == "approve":
                    position_id = int(data.get("id"))
                    if position_id:
                        position = await CRUDPosition.get(position_id=position_id)
                        await CRUDPosition.delete(position_id=position_id, parent_id=position_id)
                        await callback.answer(
                            text=f"Должность {position.name} и все её подкатегории были удалены!"
                        )
                        await callback.message.edit_text(
                            text="<b>Должности:</b>",
                            reply_markup=await list_positions_ikb()
                        )
                elif data.get("action") == "incorrect":
                    position_id = int(data.get("id"))
                    if position_id:
                        position = await CRUDPosition.get(position_id=position_id)
                        await callback.answer(
                            text=f"Удаление должности {position.name} и ее подкатегорий было отменено!"
                        )
                        await callback.message.edit_text(
                            text="<b>Должности:</b>",
                            reply_markup=await list_positions_ikb()
                        )
            # Подкатегории должностей
            elif data.get("target") == "subpositions":
                if data.get("action") == "get_all":
                    position_id = int(data.get("id"))
                    position = await CRUDPosition.get(position_id=position_id)
                    await callback.message.edit_text(
                        text=f"Подкатегории для должности <b>{position.name}</b>:",
                        reply_markup=await list_subpositions_ikb(position_id)
                    )
                elif data.get("action") == "add":
                    position_id = int(data.get("id"))
                    position = await CRUDPosition.get(position_id=position_id)
                    await state.update_data(position_id=position_id)
                    await AddSubPositionFSM.AddSubPosition.set()
                    await callback.message.edit_text(
                        text=f"Введите подкатегорию для должности <b>{position.name}</b>, которую хотите добавить:"
                    )
                elif data.get("action") == "del":
                    subposition_id = int(data.get("id"))
                    subposition = await CRUDPosition.get(position_id=subposition_id)
                    position = await CRUDPosition.get(position_id=subposition.parent_id)
                    await callback.message.edit_text(
                        text=f"Вы действительно хотите удалить подкатегорию <b>{subposition.name}</b>"
                             f" в должности <b>{position.name}</b>?",
                        reply_markup=await approve(target="subpositions", object_id=subposition_id)
                    )
                elif data.get("action") == "approve":
                    subposition_id = int(data.get("id"))
                    if subposition_id:
                        subposition = await CRUDPosition.get(position_id=subposition_id)
                        position = await CRUDPosition.get(position_id=subposition.parent_id)
                        await CRUDPosition.delete(position_id=subposition_id)
                        await callback.answer(
                            text=f"Подкатегория {subposition.name} была удалена!"
                        )
                        await callback.message.edit_text(
                            text=f"Подкатегории для должности <b>{position.name}</b>:",
                            reply_markup=await list_subpositions_ikb(position.id)
                        )
                elif data.get("action") == "incorrect":
                    if int(data.get("id")) > 0:
                        subposition_id = int(data.get("id"))
                        if subposition_id:
                            subposition = await CRUDPosition.get(position_id=subposition_id)
                            position = await CRUDPosition.get(position_id=subposition.parent_id)
                            await callback.answer(
                                text=f"Удаление подкатегории {subposition.name} для "
                                     f"должности {position.name} было отменено!"
                            )
                            await callback.message.edit_text(
                                text=f"Подкатегории для должности <b>{position.name}</b>:",
                                reply_markup=await list_subpositions_ikb(position.id)
                            )
            # Опыт работы
            elif data.get("target") == "work_experience":
                if data.get("action") == "get_all":
                    await callback.message.edit_text(
                        text="<b>Опыт работы:</b>",
                        reply_markup=await list_all_work_experience_ikb()
                    )
                elif data.get("action") == "add":
                    await AddWorkExperienceFSM.AddWorkExperience.set()
                    await callback.message.edit_text(
                        text="<b>Введите вариант опыта работы:</b>"
                    )
                elif data.get("action") == "del":
                    work_experience_id = int(data.get("id"))
                    work_experience = await CRUDWorkExperience.get(work_experience_id=work_experience_id)
                    await callback.message.edit_text(
                        text=f"Вы действительно хотите удалить данный опат работы <b>{work_experience.name}</b>?",
                        reply_markup=await approve(target="work_experience", object_id=work_experience_id)
                    )
                elif data.get("action") == "approve":
                    work_experience_id = int(data.get("id"))
                    if work_experience_id:
                        work_experience = await CRUDWorkExperience.get(work_experience_id=work_experience_id)
                        await CRUDWorkExperience.delete(work_experience_id=work_experience_id)
                        await callback.answer(
                            text=f"Вариант {work_experience.name} был удален из опыта работы!"
                        )
                        await callback.message.edit_text(
                            text="<b>Опыт работы:</b>",
                            reply_markup=await list_all_work_experience_ikb()
                        )
                elif data.get("action") == "incorrect":
                    work_experience_id = int(data.get("id"))
                    if work_experience_id:
                        work_experience = await CRUDWorkExperience.get(work_experience_id=work_experience_id)
                        await callback.answer(
                            text=f"Удаление варианта {work_experience.name} было отменено!"
                        )
                        await callback.message.edit_text(
                            text="<b>Опыт работы:</b>",
                            reply_markup=await list_all_work_experience_ikb()
                        )
            # Возраст
            elif data.get("target") == "ages":
                if data.get("action") == "get_all":
                    await callback.message.edit_text(
                        text="<b>Возраст:</b>",
                        reply_markup=await list_ages_ikb()
                    )
                elif data.get("action") == "add":
                    await AddAgeFSM.AddAge.set()
                    await callback.message.edit_text(
                        text="<b>Введите вариант возраста:</b>"
                    )
                elif data.get("action") == "del":
                    age_id = int(data.get("id"))
                    age = await CRUDAge.get(age_id=age_id)
                    await callback.message.edit_text(
                        text=f"Вы действительно хотите удалить данный возраст <b>{age.name}</b>?",
                        reply_markup=await approve(target="ages", object_id=age_id)
                    )
                elif data.get("action") == "approve":
                    age_id = int(data.get("id"))
                    if age_id:
                        age = await CRUDAge.get(age_id=age_id)
                        await CRUDAge.delete(age_id=age_id)
                        await callback.answer(
                            text=f"Вариант {age.name} был удален из возраста!"
                        )
                        await callback.message.edit_text(
                            text="<b>Возраст:</b>",
                            reply_markup=await list_ages_ikb()
                        )
                elif data.get("action") == "incorrect":
                    age_id = int(data.get("id"))
                    if age_id:
                        age = await CRUDAge.get(age_id=age_id)
                        await callback.answer(
                            text=f"Удаление варианта {age.name} было отменено!"
                        )
                        await callback.message.edit_text(
                            text="<b>Возраст:</b>",
                            reply_markup=await list_ages_ikb()
                        )
            # Статистика
            elif data.get("target") == "statistic":
                if data.get("action") == "get_all":
                    count_employers = len(await CRUDUser.get_all(role_id=3))
                    count_applicants = len(await CRUDUser.get_all(role_id=4))
                    count_all_vacancies = len(await CRUDVacancy.get_all())
                    count_open_vacancies = len(await CRUDVacancy.get_all(is_published=True))
                    count_closed_vacancies = count_all_vacancies - count_open_vacancies
                    count_all_applicant_forms = len(await CRUDApplicantForm.get_all())
                    count_open_applicant_forms = len(await CRUDApplicantForm.get_all(is_published=True))
                    count_closed_applicant_forms = count_all_applicant_forms - count_open_applicant_forms
                    text = f"<b>Статистика:</b>\n\n" \
                           f"Всего работодателей: <b>{count_employers}</b>\n" \
                           f"Всего соискателей: <b>{count_applicants}</b>\n\n" \
                           f"<b>Вакансии:</b>\n" \
                           f"Всего вакансий: <b>{count_all_vacancies}</b>\n" \
                           f"Открытых: <b>{count_open_vacancies}</b>\n" \
                           f"Закрытых: <b>{count_closed_vacancies}</b>\n\n" \
                           f"<b>Анкеты:</b>\n" \
                           f"Всего анкет: <b>{count_all_applicant_forms}</b>\n" \
                           f"Открытых: <b>{count_open_applicant_forms}</b>\n" \
                           f"Закрытых: <b>{count_closed_applicant_forms}</b>"
                    await callback.message.edit_text(
                        text=text,
                        reply_markup=await back_ikb()
                    )
            # Рассылка
            elif data.get("target") == "mailing":
                if data.get("action") == "get_all":
                    await callback.message.edit_text(
                        text="Выберите тип рассылки:",
                        reply_markup=await mailing_type_ikb()
                    )
                elif data.get("action") == "text_mailing":
                    await AddMailingFSM.AddText.set()
                    await callback.message.edit_text(
                        text="Введите текст рассылки (в формате HTML разметки):"
                    )
                elif data.get("action") == "text_and_photo_mailing":
                    await AddMailingFSM.AddPhoto.set()
                    await callback.message.edit_text(
                        text="Пришлите картинку:"
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
                # Города
                if await state.get_state() == "AddCityFSM:AddCity":
                    await state.update_data(city=message.text.strip().title())
                    await AddCityFSM.Approve.set()
                    await message.answer(
                        text=f"Проверьте правильность введенных данных:\n"
                             f"<b>{message.text.strip().title()}</b>",
                        reply_markup=await approve(target="cities")
                    )
                # Гражданства
                elif await state.get_state() == "AddCitizenshipFSM:AddCitizenship":
                    await state.update_data(citizenship=message.text.strip().title())
                    await AddCitizenshipFSM.Approve.set()
                    await message.answer(
                        text=f"Проверьте правильность введенных данных:\n"
                             f"<b>{message.text.strip().title()}</b>",
                        reply_markup=await approve(target="citizenships")
                    )
                # Должности
                elif await state.get_state() == "AddPositionFSM:AddPosition":
                    await state.update_data(position=message.text.strip().title())
                    await AddPositionFSM.Approve.set()
                    await message.answer(
                        text=f"Проверьте правильность введенных данных:\n"
                             f"<b>{message.text.strip().title()}</b>",
                        reply_markup=await approve(target="positions")
                    )
                # Подкатегории должностей
                elif await state.get_state() == "AddSubPositionFSM:AddSubPosition":
                    await state.update_data(subposition_name=message.text.strip().title())
                    await AddSubPositionFSM.Approve.set()
                    await message.answer(
                        text=f"Проверьте правильность введенных данных:\n"
                             f"<b>{message.text.strip().title()}</b>",
                        reply_markup=await approve(target="subpositions")
                    )
                # Опыт работы
                elif await state.get_state() == "AddWorkExperienceFSM:AddWorkExperience":
                    await state.update_data(work_experience=message.text.strip().title())
                    await AddWorkExperienceFSM.Approve.set()
                    await message.answer(
                        text=f"Проверьте правильность введенных данных:\n"
                             f"<b>{message.text.strip().title()}</b>",
                        reply_markup=await approve(target="work_experience")
                    )
                # Возраст
                elif await state.get_state() == "AddAgeFSM:AddAge":
                    await state.update_data(age=message.text.strip().title())
                    await AddAgeFSM.Approve.set()
                    await message.answer(
                        text=f"Проверьте правильность введенных данных:\n"
                             f"<b>{message.text.strip().title()}</b>",
                        reply_markup=await approve(target="ages")
                    )
                # Рассылка
                elif await state.get_state() == "AddMailingFSM:AddText":
                    await state.update_data(text=message.text)
                    state_data: dict = await state.get_data()
                    if state_data.get('photo_id'):
                        await AddMailingFSM.Approve.set()
                        await bot.send_photo(
                            chat_id=message.from_user.id,
                            photo=state_data.get('photo_id'),
                            caption=f"Проверьте правильность введенных данных:\n"
                                    f"{message.text}",
                            reply_markup=await approve(target="mailing"),
                            parse_mode="HTML"
                        )
                    else:
                        await AddMailingFSM.Approve.set()
                        await message.answer(
                            text=f"Проверьте правильность введенных данных:\n"
                                 f"{message.text}",
                            reply_markup=await approve(target="mailing"),
                            parse_mode="HTML"
                        )
                elif await state.get_state() == "AddMailingFSM:AddPhoto":
                    await state.update_data(photo_id=message.photo[0].file_id)
                    await AddMailingFSM.AddText.set()
                    await message.answer(
                        text="Введите текст рассылки (в формате HTML разметки):"
                    )
