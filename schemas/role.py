from pydantic import BaseModel, Field


class RoleSchema(BaseModel):
    name: str


class RoleInDBSchema(RoleSchema):
    id: int = Field(ge=1)
