"""Модуль с константами для подтверждения."""

from enum import StrEnum, auto


class ConfirmationType(StrEnum):
    """
    Тип подтверждения.

    Attributes:
        EMAIL: Подтверждение по email.
    """

    EMAIL = auto()


# Дней до истечения токена подтверждения
EXPIRED_CONFIRM_TOKEN_DAYS: int = 7
