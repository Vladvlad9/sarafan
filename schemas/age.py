from pydantic import BaseModel, Field


class AgeSchema(BaseModel):
    name: str


class AgeInDBSchema(AgeSchema):
    id: int = Field(ge=1)
