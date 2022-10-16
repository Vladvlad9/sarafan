from datetime import datetime
from pydantic import BaseModel, Field


class VacancySchema(BaseModel):
    citizenship_id: int = Field(ge=1, default=None)
    city_id: int = Field(ge=1, default=None)
    work_experience_id: int = Field(ge=1, default=None)
    age_id: int = Field(ge=1)
    english_id: int = Field(ge=1, default=None)
    position_id: int = Field(ge=1)
    is_published: bool = Field(default=False)
    date_created: datetime = Field(default=datetime.now())
    user_id: int = Field(ge=1)


class VacancyInDBSchema(VacancySchema):
    id: int = Field(ge=1)
