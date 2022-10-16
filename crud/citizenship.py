from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete

from models import CitizenShip, create_async_session
from schemas import CitizenShipInDBSchema, CitizenShipSchema


class CRUDCitizenShip(object):

    @staticmethod
    @create_async_session
    async def add(citizen_ship: CitizenShipSchema, session: AsyncSession = None) -> CitizenShipInDBSchema | None:
        citizenship = CitizenShip(**citizen_ship.dict())
        session.add(citizenship)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(citizenship)
            return CitizenShipInDBSchema(**citizenship.__dict__)

    @staticmethod
    @create_async_session
    async def delete(citizenship_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(CitizenShip)
            .where(CitizenShip.id == citizenship_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(citizenship_id: int, session: AsyncSession = None) -> CitizenShipInDBSchema | None:
        citizenship = await session.execute(
            select(CitizenShip)
            .where(CitizenShip.id == citizenship_id)
        )
        if citizenship := citizenship.first():
            return CitizenShipInDBSchema(**citizenship[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[CitizenShipInDBSchema]:
        citizen_ships = await session.execute(
            select(CitizenShip)
        )
        return [CitizenShipInDBSchema(**citizenship[0].__dict__) for citizenship in citizen_ships]

    @staticmethod
    @create_async_session
    async def update(citizenship: CitizenShipInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(CitizenShip)
            .where(CitizenShip.id == citizenship.id)
            .values(**citizenship.dict())
        )
        await session.commit()
