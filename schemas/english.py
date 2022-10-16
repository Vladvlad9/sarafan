from pydantic import BaseModel, Field


class EnglishSchema(BaseModel):
    name: str


class EnglishInDBSchema(EnglishSchema):
    id: int = Field(ge=1)
