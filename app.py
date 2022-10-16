import asyncio
from datetime import datetime

from aiogram.utils.exceptions import ChatNotFound

from crud import CRUDApplicantForm
from keyboards.inline.users import Profile
from loader import bot
from utils.set_bot_commands import set_default_commands


async def scheduler():
    while True:
        applicant_forms = list(filter(lambda x: x.is_published, await CRUDApplicantForm.get_all()))
        for applicant_form in applicant_forms:
            applicant_publish_days = (datetime.now() - applicant_form.date_created).days
            if applicant_publish_days == 10:
                applicant_form = await CRUDApplicantForm.get(user_id=applicant_form.user_id)
                applicant_form.is_published = False
                applicant_form.date_created = datetime.now()
                await CRUDApplicantForm.update(applicant_form=applicant_form)
            elif applicant_publish_days == 7:
                try:
                    await bot.send_message(
                        chat_id=applicant_form.user_id,
                        text="Ваша анкета актуальная",
                        reply_markup=await Profile.approve_ikb(target="scheduler",
                                                               user_id=applicant_form.user_id,
                                                               scheduler=True)
                    )
                    await asyncio.sleep(0.4)
                except ChatNotFound:
                    applicant_form = await CRUDApplicantForm.get(user_id=applicant_form.user_id)
                    applicant_form.is_published = False
                    applicant_form.date_created = datetime.now()
                    await CRUDApplicantForm.update(applicant_form=applicant_form)
        delay = datetime.now().date()
        delay = datetime(year=delay.year, month=delay.month, day=delay.day, hour=13) - datetime.now()
        delay = delay.seconds
        await asyncio.sleep(delay)


async def on_startup(_):
    await set_default_commands(dp)
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
