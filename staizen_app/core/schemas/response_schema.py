from pydantic import BaseModel, Field

from core.schemas.request_schema import GenericUser

class GenericResponse(BaseModel):
    success: bool = Field(...)
    code: int = Field(...)
    message: str = Field(...)
    data: dict = Field(...)

class AccountResponse(GenericResponse):
    data: GenericUser = Field(...)

class ErrorResponse(BaseModel):
    detail: str = Field(...)