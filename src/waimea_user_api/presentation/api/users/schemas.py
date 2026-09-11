from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    role_id: int = Field(gt=0)
    password: str | None = Field(default=None, min_length=8)


class CreateUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    generated_password: str | None = None