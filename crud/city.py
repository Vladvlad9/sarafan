from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import CitySchema, CityInDBSchema

from models import City, create_async_session


class CRUDCity(object):

    @staticmethod
    @create_async_session
    async def add(
            city: CitySchema,
            session: AsyncSession = None) -> CityInDBSchema | None:
        city = City(
            **city.dict()
        )
        session.add(city)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(city)
            return CityInDBSchema(**city.__dict__)

    @staticmethod
    @create_async_session
    async def delete(city_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(City)
            .where(City.id == city_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(city_id: int, session: AsyncSession = None) -> CityInDBSchema | None:
        city = await session.execute(
            select(City)
            .where(City.id == city_id)
        )
        if city := city.first():
            return CityInDBSchema(**city[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[CityInDBSchema]:
        cities = await session.execute(
            select(City)
        )
        return [CityInDBSchema(**city[0].__dict__) for city in cities]

    @staticmethod
    @create_async_session
    async def update(city: CityInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(City)
            .where(City.id == city.id)
            .values(**city.dict())
        )
        await session.commit()
