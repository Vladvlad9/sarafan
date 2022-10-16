from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, update
from models import Age, create_async_session
from schemas import AgeSchema, AgeInDBSchema


class CRUDAge(object):

    @staticmethod
    @create_async_session
    async def add(age: AgeSchema, session: AsyncSession = None) -> AgeInDBSchema | None:
        age = Age(**age.dict())
        session.add(age)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(age)
            return AgeInDBSchema(**age.__dict__)

    @staticmethod
    @create_async_session
    async def delete(age_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(Age)
            .where(Age.id == age_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(age_id: int, session: AsyncSession = None) -> AgeInDBSchema | None:
        age = await session.execute(
            select(Age)
            .where(Age.id == age_id)
        )
        if age := age.first():
            return AgeInDBSchema(**age[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[AgeInDBSchema]:
        ages = await session.execute(
            select(Age)
        )
        return [AgeInDBSchema(**age[0].__dict__) for age in ages]

    @staticmethod
    @create_async_session
    async def update(age: AgeInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(Age)
            .where(Age.id == age.id)
            .values(**age.dict())
        )
        await session.commit()
