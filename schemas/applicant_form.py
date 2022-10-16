from datetime import datetime
from pydantic import BaseModel, Field


class ApplicantFormSchema(BaseModel):
    date_of_birth: datetime
    citizenship_id: int = Field(ge=1)
    is_married: bool = Field(default=False)
    city_id: int = Field(ge=1, default=None)
    work_experience_id: int = Field(ge=1)
    phone_number: str = Field(max_length=13, default=None)
    username: str = Field(default=None)
    instagram_url: str = Field(default=None)
    knowledge_of_english: int = Field(ge=1)
    position_id: int = Field(ge=1)
    is_published: bool = Field(default=True)
    date_created: datetime = Field(default=datetime.now())
    name: str
    surname: str
    patronymic: str = Field(default=None)
    user_id: int = Field(ge=1)


class ApplicantFormInDBSchema(ApplicantFormSchema):
    id: int = Field(ge=1)
