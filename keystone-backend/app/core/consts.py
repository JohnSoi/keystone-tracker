"""Модуль базовых констант."""

from enum import StrEnum, auto

# Кодировка строк
STR_ENCODED: str = "utf-8"


class ServiceOperation(StrEnum):
    """
    Доступные операции сервиса.

    Attributes:
        CREATE: Создание.
        UPDATE: Обновление.
        DELETE: Удаление.
    """

    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()
