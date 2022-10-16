from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from models import Status, create_async_session, create_sync_session
from schemas import StatusInDBSchema


class CRUDStatus:

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[StatusInDBSchema]:
        statuses = await session.execute(
            select(Status)
        )
        return [StatusInDBSchema(**status[0].__dict__) for status in statuses]

    @staticmethod
    @create_sync_session
    def get_all_sync(session: Session = None) -> list[StatusInDBSchema]:
        statuses = session.execute(
            select(Status)
        )
        return [StatusInDBSchema(**status[0].__dict__) for status in statuses]