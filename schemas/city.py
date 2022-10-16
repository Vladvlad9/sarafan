from pydantic import BaseModel, Field


class CitySchema(BaseModel):
    name: str


class CityInDBSchema(CitySchema):
    id: int = Field(ge=1)
