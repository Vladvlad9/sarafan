from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete

from models import RecentJob, create_async_session
from schemas import RecentJobSchema, RecentJobInDBSchema


class CRUDRecentJob(object):

    @staticmethod
    @create_async_session
    async def add(recent_job: RecentJobSchema, session: AsyncSession = None) -> RecentJobInDBSchema | None:
        recent_job = RecentJob(**recent_job.dict())
        session.add(recent_job)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(recent_job)
            return RecentJobInDBSchema(**recent_job.__dict__)

    @staticmethod
    @create_async_session
    async def delete(recent_job_id: int = None, applicant_form_id: int = None, session: AsyncSession = None) -> None:
        if applicant_form_id:
            await session.execute(
                delete(RecentJob)
                .where(RecentJob.applicant_form_id == applicant_form_id)
            )
        else:
            await session.execute(
                delete(RecentJob)
                .where(RecentJob.id == recent_job_id)
            )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(recent_job_id: int = None, applicant_form_id: int = None, session: AsyncSession = None) -> RecentJobInDBSchema:
        if applicant_form_id:
            recent_job = await session.execute(
                select(RecentJob)
                .where(RecentJob.applicant_form_id == applicant_form_id)
            )
        else:
            recent_job = await session.execute(
                select(RecentJob)
                .where(RecentJob.id == recent_job_id)
            )
        if recent_job := recent_job.first():
            return RecentJobInDBSchema(**recent_job[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_name(recent_job_id: int, session: AsyncSession = None) -> list[RecentJobInDBSchema]:

        recent_job = await session.execute(
            select(RecentJob)
            .where(RecentJob.applicant_form_id == recent_job_id)
        )
        return [RecentJobInDBSchema(**recent_job[0].__dict__) for recent_job in recent_job]

    @staticmethod
    @create_async_session
    async def get_all(applicant_form_id: int = None, session: AsyncSession = None) -> list[RecentJobInDBSchema]:

        if applicant_form_id:
            recent_job = await session.execute(
                select(RecentJob)
                .where(RecentJob.applicant_form_id == applicant_form_id)
            )
        else:
            recent_jobs = await session.execute(
                select(RecentJob)
            )
        return [RecentJobInDBSchema(**recent_job[0].__dict__) for recent_job in recent_jobs]

    @staticmethod
    @create_async_session
    async def update(recent_job: RecentJobInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(RecentJob)
            .where(RecentJob.id == recent_job.id)
            .values(**recent_job.dict())
        )
        await session.commit()
