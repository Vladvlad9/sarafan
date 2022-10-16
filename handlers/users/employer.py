from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.inline.users.employer import employer_cb, Employer
from states.users import AddVacancy, InviteCandidate, EditVacancy


@dp.callback_query_handler(employer_cb.filter())
@dp.callback_query_handler(employer_cb.filter(), state=AddVacancy.all_states)
@dp.callback_query_handler(employer_cb.filter(), state=EditVacancy.all_states)
@dp.callback_query_handler(employer_cb.filter(), state=InviteCandidate.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await Employer.process(callback=callback, state=state)


@dp.message_handler(state=AddVacancy.all_states)
@dp.message_handler(state=EditVacancy.all_states)
@dp.message_handler(state=InviteCandidate.all_states)
async def process_message(message: types.Message, state: FSMContext):
    await Employer.process(message=message, state=state)
