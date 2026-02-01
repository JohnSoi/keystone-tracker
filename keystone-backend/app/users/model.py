# pylint: disable=too-few-public-methods
"""Модель пользователя."""

from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import BaseModel, SoftDeleteMixin, TimestampMixin, UUIDMixin


class User(BaseModel, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Модель пользователя.

    Attributes:
        name (str): Имя пользователя.
        surname (str): Фамилия пользователя.
        patronymic (str | None): Отчество пользователя.
        date_of_birth (date): Дата рождения пользователя.
        login (str): Логин пользователя.
        password (str): Пароль пользователя.
        email (str): Электронная почта пользователя.
        verified_at (date | None): Дата подтверждения электронной почты.

        id (int): Идентификатор пользователя.
        uuid (str): Уникальный идентификатор пользователя.
        created_at (datetime): Дата и время создания пользователя.
        updated_at (datetime): Дата и время последнего обновления пользователя.
        deleted_at (datetime | None): Дата и время удаления пользователя.
    """

    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    surname: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    patronymic: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    login: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)

    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)

    verified_at: Mapped[date | None] = mapped_column(Date, nullable=True)

    @property
    def full_name(self) -> str:
        """Возвращает полное имя пользователя."""
        return f"{self.surname} {self.name}" + (f" {self.patronymic}" if self.patronymic else "")
