from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, update

from models import English, create_async_session, create_sync_session
from models.engine import Session
from schemas import EnglishSchema, EnglishInDBSchema


class CRUDEnglish(object):

    @staticmethod
    @create_async_session
    async def add(
            english: EnglishSchema,
            session: AsyncSession = None) -> EnglishInDBSchema | None:
        english = English(
            **english.dict()
        )
        session.add(english)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(english)
            return EnglishInDBSchema(**english.__dict__)

    @staticmethod
    @create_async_session
    async def delete(english_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(English)
            .where(English.id == english_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(english_id: int, session: AsyncSession = None) -> EnglishInDBSchema | None:
        english = await session.execute(
            select(English)
            .where(English.id == english_id)
        )
        if english := english.first():
            return EnglishInDBSchema(**english[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[EnglishInDBSchema]:
        english = await session.execute(
            select(English)
        )
        return [EnglishInDBSchema(**eng[0].__dict__) for eng in english]

    @staticmethod
    @create_async_session
    async def update(english: EnglishInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(English)
            .where(English.id == english.id)
            .values(**english.dict())
        )
        await session.commit()

    @staticmethod
    @create_sync_session
    def get_all_sync(session: Session = None) -> list[EnglishInDBSchema]:
        english = session.execute(
            select(English)
        )
        return [EnglishInDBSchema(**english[0].__dict__) for english in english]