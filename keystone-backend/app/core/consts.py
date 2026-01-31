"""Модуль базовых констант."""

from enum import StrEnum, auto

# Кодировка строк
STR_ENCODED: str = "utf-8"


class ServiceOperation(StrEnum):
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()
