from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BadRequest
from keyboards.inline.users import Profile, calendar_callback
from keyboards.inline.users.employer import employer_ikb
from keyboards.inline.users.registration import register_cb, Register, DialogCalendar
from states.users import UserRegister, AddVacancy, EditVacancy, InviteCandidate, EditProfile, EditRegister
from loader import dp, bot
from crud.users import CRUDUser


@dp.message_handler(commands=["start"], state=AddVacancy.all_states)
@dp.message_handler(commands=["start"], state=EditVacancy.all_states)
@dp.message_handler(commands=["start"], state=InviteCandidate.all_states)
@dp.message_handler(commands=["start"], state=UserRegister.all_states)
@dp.message_handler(commands=["start"], state=EditRegister.all_states)
@dp.message_handler(commands=["start"], state=EditProfile.all_states)
async def stop_state_user(message: types.Message, state: FSMContext):
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
    await state.finish()
    user = await CRUDUser.get(user_id=message.from_user.id)
    if user.role_id == 4:
        await message.answer(text=f"<b>Главное меню</b>",
                             reply_markup=await Profile.profile_ikb(user_id=message.from_user.id))
    elif user.role_id == 3:
        await message.answer(
            text="Меню работодателя",
            reply_markup=await employer_ikb()
        )


@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
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

    if await CRUDUser.get(user_id=message.from_user.id):
        user = await CRUDUser.get(user_id=message.from_user.id)
        if user.role_id == 4:
            await message.answer(text=f"<b>Главное меню</b>",
                                 reply_markup=await Profile.profile_ikb(user_id=message.from_user.id))
        elif user.role_id == 3:
            await message.answer(
                text="Меню работодателя",
                reply_markup=await employer_ikb()
            )
    else:
        await message.answer(
            text="Выберите!",
            reply_markup=await Profile.looking_ikb()
        )


@dp.callback_query_handler(register_cb.filter())
@dp.callback_query_handler(register_cb.filter(), state=UserRegister.all_states)
@dp.callback_query_handler(register_cb.filter(), state=EditRegister.all_states)
async def process_callback_reg(callback: types.CallbackQuery, state: FSMContext = None):
    await Register.process(callback=callback, state=state)


@dp.callback_query_handler(calendar_callback.filter(), state=UserRegister.DateOfBirth)
async def process_calendar_reg(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    select, date = await DialogCalendar().process_selection(callback, callback_data)
    if select:
        await Register.process(callback=callback, state=state)


@dp.message_handler(state=UserRegister.all_states, content_types=["text", "contact"])
@dp.message_handler(state=EditRegister.all_states, content_types=["text", "contact"])
async def process_message_reg(message: types.Message, state: FSMContext):
    await Register.process(message=message, state=state)
