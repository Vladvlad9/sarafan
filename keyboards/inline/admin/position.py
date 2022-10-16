from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from crud.position import CRUDPosition


admin_cb = CallbackData("admin", "action", "target", "id")


async def list_positions_ikb() -> InlineKeyboardMarkup:
    all_positions = await CRUDPosition.get_all_positions()
    keyboards = [
        [
            InlineKeyboardButton(
                text=f"{position.name}",
                callback_data=admin_cb.new("get_all", "subpositions", position.id)
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=admin_cb.new("del", "positions", position.id)
            )
        ]
        for position in all_positions
    ]
    keyboards.append(
        [
            InlineKeyboardButton(text="➕", callback_data=admin_cb.new("add", "positions", 0)),
            InlineKeyboardButton(text="Назад", callback_data=admin_cb.new("back", "back_admin_menu", ""))
        ]
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard


async def list_subpositions_ikb(position_id: int) -> InlineKeyboardMarkup:
    all_subpositions = await CRUDPosition.get_all_subpositions(position_id=position_id)
    keyboards = [
        [
            InlineKeyboardButton(
                text=f"{subposition.name}",
                callback_data=" "
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=admin_cb.new("del", "subpositions", subposition.id)
            )
        ]
        for subposition in all_subpositions
    ]
    keyboards.append(
        [
            InlineKeyboardButton(text="➕", callback_data=admin_cb.new("add", "subpositions", position_id)),
            InlineKeyboardButton(text="Назад", callback_data=admin_cb.new("back", "back_positions", ""))
        ]
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboards
    )
    return keyboard

