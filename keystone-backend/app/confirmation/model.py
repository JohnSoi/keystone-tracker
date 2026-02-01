# pylint: disable=too-few-public-methods
"""Модуль модели для подтверждения."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import BaseModel, TimestampMixin, UUIDMixin
from app.users.model import User as UserModel

from .consts import ConfirmationType


class Confirmation(BaseModel, TimestampMixin, UUIDMixin):
    """
    Модель подтверждения.

    Attributes:
        user_id: ID пользователя.
        used_at: Время использования.
        user: Пользователь.
        type: Тип подтверждения.

    Properties:
        is_used: Токен использован.
    """

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[UserModel] = relationship(UserModel, lazy="joined", uselist=False, cascade="all, delete")
    used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    type: Mapped[str] = mapped_column(ENUM(ConfirmationType), nullable=False, default=ConfirmationType.EMAIL)

    @property
    def is_used(self) -> bool:
        """Проверяет, использовался ли токен."""
        return self.used_at is not None
