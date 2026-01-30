"""Модуль для работы с зависимостями подключения к БД."""

from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .db_manager import database_manager


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """
    Зависимость подключения к БД.

    Returns:
        (AsyncGenerator[AsyncSession, Any]): Асинхронная сессия базы данных.

    Examples:
        >>> from fastapi import Depends
        >>> from app.core import BaseSchema
        >>> from app.database import get_db
        >>>
        >>> async def user_register(user_data: BaseSchema, db: AsyncSession = Depends(get_db)):
        ...     ...
    """
    async for session in database_manager.get_session():
        yield session
