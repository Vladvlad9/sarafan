from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from crud.work_experiences import CRUDWorkExperience


admin_cb = CallbackData("admin", "action", "target", "id")


async def list_all_work_experience_ikb() -> InlineKeyboardMarkup:
    all_work_experience = await CRUDWorkExperience.get_all()
    keyboards = [
        [
            InlineKeyboardButton(
                text=f"{work_experience.name}",
                callback_data=f" "
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=admin_cb.new("del", "work_experience", work_experience.id)
            )
        ]
        for work_experience in all_work_experience
    ]
    keyboards.append(
        [
            InlineKeyboardButton(text="➕", callback_data=admin_cb.new("add", "work_experience", 0)),
            InlineKeyboardButton(text="Назад", callback_data=admin_cb.new("back", "back_admin_menu", ""))
        ]
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard

