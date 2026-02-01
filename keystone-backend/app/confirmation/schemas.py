"""Модуль с схемами данных для подтверждения."""

from pydantic import BaseModel

from .consts import ConfirmationType


class ConfirmationData(BaseModel):
    """
    Данные для подтверждения.

    Attributes:
        user_id: ID пользователя.
        type: Тип подтверждения.
        user_email: Email пользователя.
    """

    user_id: int
    type: ConfirmationType = ConfirmationType.EMAIL
    user_email: str
