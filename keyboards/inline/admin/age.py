from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from crud.age import CRUDAge


admin_cb = CallbackData("admin", "action", "target", "id")


async def list_ages_ikb() -> InlineKeyboardMarkup:
    all_ages = await CRUDAge.get_all()
    keyboards = [
        [
            InlineKeyboardButton(
                text=f"{age.name}",
                callback_data=f" "
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=admin_cb.new("del", "ages", age.id)
            )
        ]
        for age in all_ages
    ]
    keyboards.append(
        [
            InlineKeyboardButton(text="➕", callback_data=admin_cb.new("add", "ages", 0)),
            InlineKeyboardButton(text="Назад", callback_data=admin_cb.new("back", "back_admin_menu", ""))
        ]
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard
