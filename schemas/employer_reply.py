from pydantic import BaseModel, Field


class EmployerReplySchema(BaseModel):
    candidate_id: int = Field(ge=1)
    vacancy_id: int = Field(ge=1)


class EmployerReplyInDBSchema(EmployerReplySchema):
    id: int = Field(ge=1)
