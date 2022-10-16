from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from schemas import RoleInDBSchema
from models import Role, create_async_session, create_sync_session


class CRUDRole(object):

    @staticmethod
    @create_async_session
    async def get(role_id: int, session: AsyncSession = None) -> RoleInDBSchema | None:
        role = await session.execute(
            select(Role)
            .where(Role.id == role_id)
        )
        if role := role.first():
            return RoleInDBSchema(**role[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[RoleInDBSchema]:
        roles = await session.execute(
            select(Role)
        )
        return [RoleInDBSchema(**role[0].__dict__) for role in roles]

    @staticmethod
    @create_sync_session
    def get_all_sync(session: Session = None) -> list[RoleInDBSchema]:
        roles = session.execute(
            select(Role)
        )
        return [RoleInDBSchema(**role[0].__dict__) for role in roles]
