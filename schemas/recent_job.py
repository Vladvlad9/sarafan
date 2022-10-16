from pydantic import BaseModel, Field


class RecentJobSchema(BaseModel):
    applicant_form_id: int = Field(ge=1)
    name: str


class RecentJobInDBSchema(RecentJobSchema):
    id: int = Field(ge=1)
