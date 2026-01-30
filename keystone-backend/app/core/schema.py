"""Модуль базовых схем приложения."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    Базовая схема данных.

    Attributes:
        id (int): Идентификатор объекта (pk).

    Examples:
        >>> class UserSchema(BaseSchema):
        ...     name: str
        >>>
        >>> UserSchema(id=1, name="John")
    """

    id: int


class TimeStampSchemaMixin(BaseModel):
    """
    Базовая схема данных с полями для хранения даты создания и обновления объекта.

    Attributes:
        created_at (datetime): Дата создания объекта.
        updated_at (datetime): Дата обновления объекта.

    Examples:
        >>> class UserSchema(TimeStampSchemaMixin):
        ...     name: str
        >>>
        >>> UserSchema(name="John", created_at=datetime.now(), updated_at=datetime.now())
    """

    created_at: datetime
    updated_at: datetime


class SoftDeleteSchemaMixin(BaseModel):
    """
    Базовая схема данных с полем для хранения даты удаления объекта.

    Attributes:
        deleted_at (datetime | None): Дата удаления объекта.

    Examples:
        >>> class UserSchema(SoftDeleteSchemaMixin):
        ...     name: str
        >>>
        >>> UserSchema(name="John", deleted_at=datetime.now())
    """

    deleted_at: datetime | None


class UUIDSchemaMixin(BaseModel):
    """
    Базовая схема данных с полем для хранения UUID объекта.

    Attributes:
        uuid (UUID): UUID объекта.

    Examples:
        >>> from uuid import uuid4
        >>>
        >>> class UserSchema(UUIDSchemaMixin):
        ...     name: str
        >>>
        >>> UserSchema(name="John", uuid=uuid4())
    """

    uuid: UUID
