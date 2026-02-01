"""Модуль с типами."""

from typing import TypeVar

from pydantic import BaseModel

from app.core.database import BaseRepository

# Тип для репозитория
Repository = TypeVar("Repository", bound=BaseRepository)
# Тип входных данных
InputData = TypeVar("InputData", bound=BaseModel)
