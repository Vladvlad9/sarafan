from json import dumps

import aiohttp

from crud import CRUDCitizenShip, CRUDPosition, CRUDCity, CRUDWorkExperience, CRUDEnglish
from schemas import ApplicantFormInDBSchema, VacancyInDBSchema
from utils import Page


class TelegraphPage():
    def __init__(self, token: str) -> None:
        self.token = token
        self.timeout = 5

    async def create_page(self, form: VacancyInDBSchema) -> Page | None:
        async with aiohttp.ClientSession(base_url='https://api.telegra.ph') as session:
            citizenship = await CRUDCitizenShip.get(citizenship_id=form.citizenship_id)
            position = await CRUDPosition.get(position_id=form.position_id)
            city = await CRUDCity.get(city_id=form.city_id)
            work_experience = await CRUDWorkExperience.get(
                work_experience_id=form.work_experience_id)
            english = await CRUDEnglish.get(english_id=form.english_id)

            text = f"Вакансия: {position.name}\n" \
                   f"Гражданство: {citizenship.name}\n" \
                   f"Город: {city.name}\n" \
                   f"Опыт работы: {work_experience.name}\n" \
                   f"Знание английского языка: {english.name}\n\n"\
                   f"Тут будет кратко описана информация о профессии "
            params = {
                "content": dumps([{"tag": "p", "children": [text]}]),
                "title": position.name
            }
            data = await session.post('/createPage', params=params | {"access_token": self.token})
            return await data.json()
