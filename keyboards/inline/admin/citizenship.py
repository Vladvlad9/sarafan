from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from crud.citizenship import CRUDCitizenShip


admin_cb = CallbackData("admin", "action", "target", "id")


async def list_all_citizenships_ikb() -> InlineKeyboardMarkup:
    all_citizenships = await CRUDCitizenShip.get_all()
    keyboards = [
        [
            InlineKeyboardButton(
                text=f"{citizenship.name}",
                callback_data=f" "
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=admin_cb.new("del", "citizenships", citizenship.id)
            )
        ]
        for citizenship in all_citizenships
    ]
    keyboards.append(
        [
            InlineKeyboardButton(text="➕", callback_data=admin_cb.new("add", "citizenships", 0)),
            InlineKeyboardButton(text="Назад", callback_data=admin_cb.new("back", "back_admin_menu", ""))
        ]
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard
