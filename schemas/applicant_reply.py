from pydantic import BaseModel, Field


class ApplicantReplySchema(BaseModel):
    user_id: int = Field(ge=1)
    vacancy_id: int = Field(ge=1)
    status_id: int = Field(ge=1)


class ApplicantReplyInDBSchema(ApplicantReplySchema):
    id: int = Field(ge=1)