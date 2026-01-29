from datetime import date

from pydantic import BaseModel, field_validator, Field

from app.core import UUIDSchemaMixin
from app.users.validators import validate_email, validate_birth_date


class UserPersonData(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    surname: str = Field(..., min_length=2, max_length=50)
    patronymic: str | None = Field(..., min_length=2, max_length=50)
    date_of_birth: date
    email: str = Field(..., min_length=6, max_length=50)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return validate_email(value)

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date) -> date:
        return validate_birth_date(value)


class UserAccessData(BaseModel):
    login: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8, max_length=50)


class UserPublicData(UUIDSchemaMixin, UserPersonData):
    ...


class UserRegisterData(UserPersonData, UserAccessData):
    ...
