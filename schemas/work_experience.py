from pydantic import BaseModel, Field


class WorkExperienceSchema(BaseModel):
    name: str


class WorkExperienceInDBSchema(WorkExperienceSchema):
    id: int = Field(ge=1)
