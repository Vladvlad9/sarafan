from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete

from models import ApplicantReply, create_async_session
from schemas import ApplicantReplySchema, ApplicantReplyInDBSchema


class CRUDApplicantReply(object):

    @staticmethod
    @create_async_session
    async def add(
            applicant_reply: ApplicantReplySchema,
            session: AsyncSession = None
    ) -> ApplicantReplyInDBSchema | None:
        applicant_reply = ApplicantReply(
            **applicant_reply.dict()
        )
        session.add(applicant_reply)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(applicant_reply)
            return ApplicantReplyInDBSchema(**applicant_reply.__dict__)

    @staticmethod
    @create_async_session
    async def delete(applicant_reply_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(ApplicantReply)
            .where(ApplicantReply.id == applicant_reply_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(applicant_reply_id: int = None,
                  vacancy_id: int = None,
                  user_id: int = None,
                  session: AsyncSession = None) -> ApplicantReplyInDBSchema | None:
        if vacancy_id:
            applicant_reply = await session.execute(
                select(ApplicantReply)
                .where(ApplicantReply.vacancy_id == vacancy_id)
            )
        elif applicant_reply_id:
            applicant_reply = await session.execute(
                select(ApplicantReply)
                .where(ApplicantReply.id == applicant_reply_id)
            )
        else:
            applicant_reply = await session.execute(
                select(ApplicantReply)
                .where(ApplicantReply.vacancy_id == user_id)
            )

        if applicant_reply := applicant_reply.first():
            return ApplicantReplyInDBSchema(**applicant_reply[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(user_id: int = None,
                      vacancy_id: int = None,
                      session: AsyncSession = None) -> list[ApplicantReplyInDBSchema]:
        if user_id:
            applicant_replies = await session.execute(
                select(ApplicantReply).where(ApplicantReply.user_id == user_id)
            )
        elif vacancy_id:
            applicant_replies = await session.execute(
                select(ApplicantReply).where(ApplicantReply.vacancy_id == vacancy_id)
            )
        else:
            applicant_replies = await session.execute(
                select(ApplicantReply)
            )
        return [ApplicantReplyInDBSchema(**applicant_reply[0].__dict__) for applicant_reply in applicant_replies]

    @staticmethod
    @create_async_session
    async def update(
            applicant_reply: ApplicantReplyInDBSchema,
            session: AsyncSession = None) -> None:
        await session.execute(
            update(ApplicantReply)
            .where(ApplicantReply.id == applicant_reply.id)
            .values(**applicant_reply.dict())
        )
        await session.commit()