from pydantic import BaseModel, Field


class CitizenShipSchema(BaseModel):
    name: str


class CitizenShipInDBSchema(CitizenShipSchema):
    id: int = Field(ge=1)
