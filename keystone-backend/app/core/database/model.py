# mypy: disable_error_code="arg-type"
"""Модуль базовой модели."""

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, declarative_base, declared_attr, mapped_column

from app.core.utils import camel_case_to_snake_case


class CustomModel:
    """
    Базовая модель. Все модели должны наследоваться от нее.

    Attributes:
        id (int): Идентификатор сущности.
    """

    __allow_unmapped__ = True

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Автоматически генерирует имя таблицы.

        Returns:
            (str): Имя таблицы.
        """
        return camel_case_to_snake_case(cls.__name__) + "s"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    def to_dict(self) -> dict:
        """
        Преобразование объекта в словарь.

        Returns:
            (dict): Словарь с атрибутами объекта.
        """
        result = {}

        for key in dir(self):
            if not key.startswith("_"):
                value = getattr(self, key)
                if not callable(value):
                    result[key] = value

        return result


# Базовая модель SQLAlchemy
BaseModel = declarative_base(cls=CustomModel)
