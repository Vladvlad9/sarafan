from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def send_contact() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='Поделиться контактом', request_contact=True),
                KeyboardButton(text='Продолжить без номера телефона', callback_data="no_phone"),
            ]
        ]
    )


async def instagram() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='Продолжить без инстаграма', callback_data="no instagram")
            ]
        ]
    )


async def nextKb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='Продолжить')
            ]
        ]
    )


async def patronymic() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='Продолжить без отчества', callback_data="no")
            ]
        ]
    )
