from pydantic import BaseModel, Field


class PositionSchema(BaseModel):
    parent_id: int = Field(ge=1, default=None)
    name: str


class PositionInDBSchema(PositionSchema):
    id: int = Field(ge=1)
