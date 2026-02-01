"""Модуль схемы данных для восстановления доступа."""

from pydantic import BaseModel


class AccessRestoreData(BaseModel):
    """
    Схема данных для восстановления доступа.

    Attributes:
        user_id (int): Идентификатор пользователя.
        user_deleted (bool): Флаг, указывающий на удаление пользователя.
        user_email (str): Электронная почта пользователя.
    """

    user_id: int
    user_deleted: bool
    user_email: str
