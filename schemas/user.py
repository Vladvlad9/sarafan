from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    role_id: int = Field(ge=1, default=None)
    id: int = Field(ge=1)


class UserInDBSchema(UserSchema):
    id: int = Field(ge=1)
