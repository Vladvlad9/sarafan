from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from crud.city import CRUDCity


admin_cb = CallbackData("admin", "action", "target", "id")


async def list_cities_ikb() -> InlineKeyboardMarkup:
    all_cities = await CRUDCity.get_all()
    keyboards = [
        [
            InlineKeyboardButton(
                text=f"{city.name}",
                callback_data=f" "
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=admin_cb.new("del", "cities", city.id)
            )
        ]
        for city in all_cities
    ]
    keyboards.append(
        [
            InlineKeyboardButton(text="➕", callback_data=admin_cb.new("add", "cities", 0)),
            InlineKeyboardButton(text="Назад", callback_data=admin_cb.new("back", "back_admin_menu", ""))
        ]
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard

