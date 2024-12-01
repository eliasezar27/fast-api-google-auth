from pydantic import BaseModel, Field

from core.schemas.request_schema import GenericUser

# Nested model for response data
class AuthData(BaseModel):
    access_token: str
    token_type: str
    user_id: str

class GenericResponse(BaseModel):
    success: bool = Field(...)
    code: int = Field(...)
    message: str = Field(...)
    data: dict | AuthData = Field(...)

class AccountResponse(GenericResponse):
    data: GenericUser = Field(...)

class ErrorResponse(BaseModel):
    detail: str = Field(...)