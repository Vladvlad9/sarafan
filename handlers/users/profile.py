from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest

from config import CONFIG
from crud import CRUDVacancy, CRUDApplicantForm, CRUDCitizenShip, CRUDPosition, CRUDCity, CRUDWorkExperience, \
    CRUDEnglish
from crud.applicant_reply import CRUDApplicantReply
from enums import Statuses
from keyboards.inline.users import Profile, profile_cb, calendar_callback, DialogCalendar
from loader import dp, bot
from states.users import EditProfile
from utils.telegraph_library import TelegraphPage


@dp.message_handler(commands=["vacancies"])
async def show_vacancies(message: types.Message):
    await message.delete()
    for entity in message.entities:
        if entity.type in ["url", "text_link"]:
            await message.delete()
        try:
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=message.message_id - 1
            )
        except BadRequest:
            pass

    applicant_replies_id: list = list(
        map(lambda x: x.vacancy_id, await CRUDApplicantReply.get_all(user_id=message.from_user.id))
    )

    vacancies: list = await CRUDVacancy.get_all(is_published=True)
    vacancies = list(filter(lambda x: x.id not in applicant_replies_id, vacancies))

    get_vacancies: list = []
    applicant_forms: list = await CRUDApplicantForm.get_all(user_id=message.from_user.id)
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
                        f"<b>Английский</b>: {english.name}\n"

        form = get_vacancies[0]
        posting = TelegraphPage(CONFIG.TELEGRAPH)
        url = await posting.create_page(form=form)
        telegraph = f"<a href='{url['result']['url']}'>Подробнее</a>"

        await message.answer(text=f"{str(vacancies_txt)}\n{telegraph}",
                             reply_markup=await Profile.orders_iter_ikb(
                                 target="page_vacancies",
                                 user_id=message.from_user.id,
                                 vacancies=get_vacancies),
                             disable_web_page_preview=True
                             )
    else:
        await message.answer("Активных вакансий нету")


@dp.message_handler(commands=["help"])
async def show_help(message: types.Message):
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except BadRequest:
        pass
    await message.delete()
    text = f"\n\n" \
           f"📱 Контактный номер телефона : {CONFIG.SUPPORT.PHONE}\n\n" \
           f"📧 Email: {CONFIG.SUPPORT.EMAIL}\n\n" \
           f"📷 Instagram : <a href='www.instagram.com/{CONFIG.SUPPORT.INSTAGRAM}/'>{CONFIG.SUPPORT.INSTAGRAM}</a>\n\n" \
           f"🎧 Discord :<code>{CONFIG.SUPPORT.DISCORD}</code>\n\n"
    await message.answer(text=f"Способ связи: {text}",
                         reply_markup=await Profile.support_ikb(),
                         parse_mode="HTML")


@dp.message_handler(commands=["responses"])
async def show_responses(message: types.Message):
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except BadRequest:
        pass

    await message.delete()
    responses = await CRUDApplicantReply.get_all(user_id=message.from_user.id)
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

        await message.answer(text=str(vacancies_txt),
                             reply_markup=await Profile.orders_iter_ikb(
                                 target="page_responses",
                                 user_id=message.from_user.id,
                                 responses=True)
                             )
    else:
        await message.answer(text="Вы не откликались на вакансии")


@dp.callback_query_handler(profile_cb.filter())
@dp.callback_query_handler(profile_cb.filter(), state=EditProfile.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await Profile.process_profile(callback=callback, state=state)


@dp.callback_query_handler(calendar_callback.filter(), state=EditProfile.DateOfBirth)
async def process_calendar(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    select, date = await DialogCalendar().process_selection(callback, callback_data)
    if select:
        await Profile.process_profile(callback=callback, state=state)


@dp.message_handler(state=EditProfile.all_states, content_types=["text", "contact"])
async def process_message(message: types.Message, state: FSMContext = None):
    await Profile.process_profile(message=message, state=state)
