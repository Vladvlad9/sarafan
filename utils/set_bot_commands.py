from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Войти"),
        types.BotCommand("vacancies", "Смотреть вакансии"),
        types.BotCommand("employers", "Работадатели"),
        types.BotCommand("ribbon", "Лента"),
        types.BotCommand("premium", "Сарафан премиум"),
        types.BotCommand("settings", "Изменения настройки профиля"),
        types.BotCommand("responses", "Посмотреть свои отклики"),
        types.BotCommand("help", "Поддержка"),
    ])
