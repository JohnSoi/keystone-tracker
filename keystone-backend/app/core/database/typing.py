"""Модуль с типами."""

from typing import TypeVar

from .model import BaseModel

# Тип модели.
DataModel = TypeVar("DataModel", bound=BaseModel)
