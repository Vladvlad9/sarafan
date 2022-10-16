from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete

from models import EmployerReply, create_async_session
from schemas import EmployerReplySchema, EmployerReplyInDBSchema


class CRUDEmployerReply(object):

    @staticmethod
    @create_async_session
    async def add(
            employer_reply: EmployerReplySchema,
            session: AsyncSession = None
    ) -> EmployerReplyInDBSchema | None:
        employer_reply = EmployerReply(
            **employer_reply.dict()
        )
        session.add(employer_reply)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(employer_reply)
            return EmployerReplyInDBSchema(**employer_reply.__dict__)

    @staticmethod
    @create_async_session
    async def delete(employer_reply_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(EmployerReply)
            .where(EmployerReply.id == employer_reply_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(employer_reply_id: int = None,
                  vacancy_id: int = None,
                  session: AsyncSession = None) -> EmployerReplyInDBSchema | None:
        if vacancy_id:
            employer_reply = await session.execute(
                select(EmployerReply)
                .where(EmployerReply.vacancy_id == vacancy_id)
            )
        else:
            employer_reply = await session.execute(
                select(EmployerReply)
                .where(EmployerReply.id == employer_reply_id)
            )
        if employer_reply := employer_reply.first():
            return EmployerReplyInDBSchema(**employer_reply[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_candidate_for_vacancy(candidate_id: int,
                                        vacancy_id: int,
                                        session: AsyncSession = None) -> EmployerReplyInDBSchema | None:
        employer_reply = await session.execute(
            select(EmployerReply)
            .where(EmployerReply.candidate_id == candidate_id)
            .where(EmployerReply.vacancy_id == vacancy_id)
        )
        if employer_reply := employer_reply.first():
            return EmployerReplyInDBSchema(**employer_reply[0].__dict__)
