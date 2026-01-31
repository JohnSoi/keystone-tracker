# pylint: disable=unnecessary-ellipsis
"""Модуль схем данных для работы с пользователями."""

from datetime import date

from pydantic import BaseModel, Field, field_validator

from app.core import UUIDSchemaMixin
from app.users.validators import validate_birth_date, validate_email


class UserPersonData(BaseModel):
    """
    Схема данных пользователя.

    Attributes:
        name (str): Имя пользователя.
        surname (str): Фамилия пользователя.
        patronymic (str | None): Отчество пользователя.
        date_of_birth (date): Дата рождения пользователя.
        email (str): Электронная почта пользователя.

    Methods:
        validate_email: Валидация электронной почты.
        validate_date_of_birth: Валидация даты рождения.
    """

    name: str = Field(..., min_length=2, max_length=50)
    surname: str = Field(..., min_length=2, max_length=50)
    patronymic: str | None = Field(..., min_length=2, max_length=50)
    date_of_birth: date
    email: str = Field(..., min_length=6, max_length=50)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Валидация электронной почты."""
        return validate_email(value)

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date) -> date:
        """Валидация даты рождения."""
        return validate_birth_date(value)


class UserPasswordData(BaseModel):
    """
    Схема данных для изменения пароля пользователя.

    Attributes:
        password (str): Пароль пользователя.
    """

    password: str = Field(..., min_length=8, max_length=50)


class UserAccessData(UserPasswordData):
    """
    Схема данных для доступа пользователя.

    Attributes:
        login (str): Логин пользователя.
        password (str): Пароль пользователя.
    """

    login: str = Field(..., min_length=3, max_length=32)


class UserPublicData(UUIDSchemaMixin, UserPersonData):
    """
    Публичная схема данных пользователя.

    Attributes:
        uuid (str): Уникальный идентификатор пользователя.
        name (str): Имя пользователя.
        surname (str): Фамилия пользователя.
        patronymic (str | None): Отчество пользователя.
        date_of_birth (date): Дата рождения пользователя.
        email (str): Электронная почта пользователя.

    Methods:
        validate_email: Валидация электронной почты.
        validate_date_of_birth: Валидация даты рождения.
    """

    ...


class UserRegisterData(UserPersonData, UserAccessData):
    """
    Схема данных для регистрации пользователя.

    Attributes:
        name (str): Имя пользователя.
        surname (str): Фамилия пользователя.
        patronymic (str | None): Отчество пользователя.
        date_of_birth (date): Дата рождения пользователя.
        email (str): Электронная почта пользователя.
        login (str): Логин пользователя.
        password (str): Пароль пользователя.

    Methods:
        validate_email: Валидация электронной почты.
        validate_date_of_birth: Валидация даты рождения.
    """

    ...


class UserAuthResponseData(BaseModel):
    """
    Схема данных ответа для аутентификации пользователя.

    Attributes:
        access_token (str): Токен доступа.
        refresh_token (str): Токен обновления.
        token_type (str): Тип токена.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
