from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, update

from models import WorkExperience, create_async_session
from schemas import WorkExperienceInDBSchema, WorkExperienceSchema


class CRUDWorkExperience(object):

    @staticmethod
    @create_async_session
    async def add(work_experience: WorkExperienceSchema, session: AsyncSession = None) -> WorkExperienceInDBSchema | None:
        work_experience = WorkExperience(**work_experience.dict())
        session.add(work_experience)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(work_experience)
            return WorkExperienceInDBSchema(**work_experience.__dict__)

    @staticmethod
    @create_async_session
    async def delete(work_experience_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(WorkExperience)
            .where(WorkExperience.id == work_experience_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(work_experience_id: int, session: AsyncSession = None) -> WorkExperienceInDBSchema | None:

        work_experience = await session.execute(
            select(WorkExperience)
            .where(WorkExperience.id == work_experience_id)
        )
        if work_experience := work_experience.first():
            return WorkExperienceInDBSchema(**work_experience[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[WorkExperienceInDBSchema]:
        work_experiences = await session.execute(
            select(WorkExperience)
        )
        return [WorkExperienceInDBSchema(**work_experience[0].__dict__) for work_experience in work_experiences]

    @staticmethod
    @create_async_session
    async def update(work_experiences: WorkExperienceInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(WorkExperience)
            .where(WorkExperience.id == work_experiences.id)
            .values(**work_experiences.dict())
        )
        await session.commit()
