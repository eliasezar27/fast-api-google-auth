from pydantic import BaseModel, EmailStr, Field


class GenericUser(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)