# pylint: disable=not-callable, too-few-public-methods
"""Модуль миксинов для моделей."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as PG_UUID
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """
    Mixin для добавления полей created_at и updated_at в модели.

    Attributes:
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.
    """

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class SoftDeleteMixin:
    """
    Mixin для добавления поля deleted_at в модели.

    Attributes:
        deleted_at (datetime): Дата и время удаления записи.
    """

    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class UUIDMixin:
    """
    Mixin для добавления поля uuid в модели.

    Attributes:
        uuid (UUID): Уникальный идентификатор записи.
    """

    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, default=uuid4, unique=True)
