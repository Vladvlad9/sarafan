from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest
from loader import dp, bot
from filters import IsAdmin
from keyboards.inline import admin_cb, AdminPanel
from states.admins import AddCityFSM, AddCitizenshipFSM, AddPositionFSM, AddSubPositionFSM, AddWorkExperienceFSM, \
    AddMailingFSM, AddAgeFSM


@dp.message_handler(IsAdmin(), commands=["start"], state=AddCityFSM.all_states)
@dp.message_handler(IsAdmin(), commands=["start"], state=AddCitizenshipFSM.all_states)
@dp.message_handler(IsAdmin(), commands=["start"], state=AddPositionFSM.all_states)
@dp.message_handler(IsAdmin(), commands=["start"], state=AddSubPositionFSM.all_states)
@dp.message_handler(IsAdmin(), commands=["start"], state=AddWorkExperienceFSM.all_states)
@dp.message_handler(IsAdmin(), commands=["start"], state=AddMailingFSM.all_states)
@dp.message_handler(IsAdmin(), commands=["start"], state=AddAgeFSM.all_states)
async def stop_state_admin(message: types.Message, state: FSMContext):
    await message.delete()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except BadRequest:
        pass
    await state.finish()
    await message.answer(
        text=f"<b>Админ панель!</b>",
        reply_markup=await AdminPanel.start()
    )


@dp.message_handler(IsAdmin(), commands=["admin"])
async def sing_in_admin_menu(message: types.Message):
    await message.delete()
    await message.answer(
        text=f"<b>{message.from_user.full_name}</b>, вы вошли в админ панель.",
        reply_markup=await AdminPanel.start()
    )


@dp.callback_query_handler(IsAdmin(), admin_cb.filter())
@dp.callback_query_handler(IsAdmin(), admin_cb.filter(), state=AddCityFSM.all_states)
@dp.callback_query_handler(IsAdmin(), admin_cb.filter(), state=AddCitizenshipFSM.all_states)
@dp.callback_query_handler(IsAdmin(), admin_cb.filter(), state=AddPositionFSM.all_states)
@dp.callback_query_handler(IsAdmin(), admin_cb.filter(), state=AddSubPositionFSM.all_states)
@dp.callback_query_handler(IsAdmin(), admin_cb.filter(), state=AddWorkExperienceFSM.all_states)
@dp.callback_query_handler(IsAdmin(), admin_cb.filter(), state=AddMailingFSM.all_states)
@dp.callback_query_handler(IsAdmin(), admin_cb.filter(), state=AddAgeFSM.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await AdminPanel.process(callback=callback, state=state)


@dp.message_handler(IsAdmin(), state=AddCityFSM.all_states)
@dp.message_handler(IsAdmin(), state=AddCitizenshipFSM.all_states)
@dp.message_handler(IsAdmin(), state=AddPositionFSM.all_states)
@dp.message_handler(IsAdmin(), state=AddSubPositionFSM.all_states)
@dp.message_handler(IsAdmin(), state=AddWorkExperienceFSM.all_states)
@dp.message_handler(IsAdmin(), state=AddMailingFSM.all_states)
@dp.message_handler(IsAdmin(), state=AddAgeFSM.all_states)
@dp.message_handler(IsAdmin(), content_types=['photo'], state=AddMailingFSM.all_states)
async def process_message(message: types.Message, state: FSMContext):
    await AdminPanel.process(message=message, state=state)
