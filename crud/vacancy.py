from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from models import Vacancy, create_async_session
from schemas.vacancy import VacancySchema, VacancyInDBSchema


class CRUDVacancy(object):

    @staticmethod
    @create_async_session
    async def add(
            vacancy: VacancySchema,
            session: AsyncSession = None
    ) -> VacancyInDBSchema | None:
        vacancy = Vacancy(
            **vacancy.dict()
        )
        session.add(vacancy)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(vacancy)
            return VacancyInDBSchema(**vacancy.__dict__)

    @staticmethod
    @create_async_session
    async def delete(vacancy_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(Vacancy)
            .where(Vacancy.id == vacancy_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(vacancy_id: int = None,
                  user_id: int = None,
                  position_id: int = None,
                  session: AsyncSession = None) -> VacancyInDBSchema | None:
        if user_id:
            vacancy = await session.execute(
                select(Vacancy)
                .where(Vacancy.user_id == user_id)
            )
        elif position_id:
            vacancy = await session.execute(
                select(Vacancy)
                .where(Vacancy.position_id == position_id)
                .where(Vacancy.id == vacancy_id)
            )
        else:
            vacancy = await session.execute(
                select(Vacancy)
                .where(Vacancy.id == vacancy_id)
            )
        if vacancy := vacancy.first():
            return VacancyInDBSchema(**vacancy[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(is_published: bool = None,
                      session: AsyncSession = None) -> list[VacancyInDBSchema]:
        if is_published:
            vacancies = await session.execute(
                select(Vacancy)
                .where(Vacancy.is_published == True)
            )
        else:
            vacancies = await session.execute(
                select(Vacancy)
            )
        return [VacancyInDBSchema(**vacancy[0].__dict__) for vacancy in vacancies]

    @staticmethod
    @create_async_session
    async def get_vacancies_employer(user_id: int, session: AsyncSession = None) -> list[VacancyInDBSchema]:
        vacancies = await session.execute(
            select(Vacancy)
            .where(Vacancy.user_id == user_id)
        )
        return [VacancyInDBSchema(**vacancy[0].__dict__) for vacancy in vacancies]

    @staticmethod
    @create_async_session
    async def update(
            vacancy: VacancyInDBSchema,
            session: AsyncSession = None) -> None:
        await session.execute(
            update(Vacancy)
            .where(Vacancy.id == vacancy.id)
            .values(**vacancy.dict())
        )
        await session.commit()
