from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, VARCHAR, Integer, Boolean, Text, ForeignKey, CHAR, BigInteger, SmallInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ApplicantForm(Base):
    __tablename__: str = "applicant_forms"

    id = Column(Integer, primary_key=True)
    date_of_birth = Column(TIMESTAMP, nullable=False)
    citizenship_id = Column(Integer, ForeignKey("citizen_ships.id", ondelete="NO ACTION"), nullable=False)
    is_married = Column(Boolean, default=False, nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="NO ACTION"), nullable=True)
    work_experience_id = Column(Integer, ForeignKey("work_experiences.id", ondelete="NO ACTION"), nullable=False)
    phone_number = Column(CHAR(12), nullable=True)
    username = Column(Text, nullable=True)
    instagram_url = Column(Text, nullable=True)
    knowledge_of_english = Column(Integer, ForeignKey("english.id", ondelete="NO ACTION"), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="NO ACTION"), nullable=False)
    is_published = Column(Boolean, default=True)
    date_created = Column(TIMESTAMP, default=datetime.now())
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    patronymic = Column(Text, nullable=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="NO ACTION"), nullable=False)


class CitizenShip(Base):
    __tablename__: str = "citizen_ships"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)


class English(Base):
    __tablename__: str = "english"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)


class City(Base):
    __tablename__: str = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)


class WorkExperience(Base):
    __tablename__: str = "work_experiences"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(10), unique=True, nullable=False)


class RecentJob(Base):
    __tablename__: str = "recent_jobs"

    id = Column(Integer, primary_key=True)
    applicant_form_id = Column(Integer, ForeignKey("applicant_forms.id", ondelete="NO ACTION"), nullable=False)
    name = Column(Text, nullable=False)


class Position(Base):
    __tablename__: str = "positions"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("positions.id", ondelete="NO ACTION"), nullable=True)
    name = Column(Text, nullable=False)


class User(Base):
    __tablename__: str = "users"

    id = Column(BigInteger, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="NO ACTION"), nullable=False)


class Role(Base):
    __tablename__: str = "roles"

    id = Column(SmallInteger, primary_key=True)
    name = Column(Text, unique=True, nullable=False)


class Vacancy(Base):
    __tablename__: str = "vacancies"

    id = Column(Integer, primary_key=True)
    citizenship_id = Column(Integer, ForeignKey("citizen_ships.id", ondelete="NO ACTION"), nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="NO ACTION"), nullable=True)
    work_experience_id = Column(Integer, ForeignKey("work_experiences.id", ondelete="NO ACTION"), nullable=True)
    age_id = Column(Integer, ForeignKey("ages.id", ondelete="NO ACTION"), nullable=False)
    english_id = Column(Integer, ForeignKey("english.id", ondelete="NO ACTION"), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="NO ACTION"), nullable=False)
    is_published = Column(Boolean, default=False)
    date_created = Column(TIMESTAMP, default=datetime.now())
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="NO ACTION"), nullable=False)


class Status(Base):
    __tablename__: str = "statuses"

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(10), unique=True, nullable=True)


class ApplicantReply(Base):
    __tablename__: str = "applicant_replies"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id", ondelete="CASCADE"), nullable=False)
    status_id = Column(SmallInteger, ForeignKey("statuses.id", ondelete="NO ACTION"), nullable=False)


class EmployerReply(Base):
    __tablename__: str = "employer_replies"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id", ondelete="CASCADE"), nullable=False)


class Age(Base):
    __tablename__: str = "ages"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(20), unique=True, nullable=False)
