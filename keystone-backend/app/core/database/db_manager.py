# pylint: disable=broad-exception-raised
"""Модуль для работы с базой данных."""

from typing import Any, AsyncGenerator

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import AppSettings, get_app_settings

from .exceptions import SessionNotCreatedException

app_settings: AppSettings = get_app_settings()


class DatabaseManager:
    """
    Менеджер для работы с базой данных.

    Attributes:
        _db_url (str): URL базы данных.
        _engine ( | None): Асинхронный движок базы данных.
        _session (async_sessionmaker[AsyncSession] | None): Асинхронная сессия базы данных.
    """

    def __init__(self, db_url: str | PostgresDsn) -> None:
        """
        Инициализирует менеджер базы данных.

        Args:
            db_url(str | PostgresDsn): URL базы данных.
        """
        self._db_url: str = str(db_url)
        self._engine: AsyncEngine | None = None
        self._session: async_sessionmaker[AsyncSession] | None = None

    def initialize(self) -> None:
        """
        Инициализирует базу данных.

        Examples:
            >>> from contextlib import asynccontextmanager
            >>> from fastapi import FastAPI
            >>> from app.core.database import database_manager
            >>>
            >>> @asynccontextmanager
            >>> async def lifespan(_: FastAPI) -> None:
            ...     database_manager.initialize()
            ...     yield
            ...     await database_manager.close()
        """
        try:
            self._engine = create_async_engine(
                self._db_url, echo=app_settings.DEBUG, pool_pre_ping=True, pool_recycle=3600
            )
            self._session = async_sessionmaker(
                self._engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False
            )
        except Exception as e:
            raise Exception(f"Failed to initialize database: {e}") from e

    async def get_session(self) -> AsyncGenerator[Any, Any]:
        """
        Возвращает сессию базы данных.

        Returns:
            (AsyncGenerator[Any, Any]): Асинхронная сессия базы данных.

        Examples:
            >>> from app.core.database import database_manager
            >>> async def get_db():
            ...     async for ex_session in database_manager.get_session():
            ...         yield ex_session

        Raises:
            SessionNotCreatedException: Если сессия не создана.
        """
        if self._session is None:
            raise SessionNotCreatedException()

        async with self._session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self) -> None:
        """
        Закрывает соединение с базой данных.

        Examples:
            >>> from contextlib import asynccontextmanager
            >>> from fastapi import FastAPI
            >>> from app.core.database import database_manager
            >>>
            >>> @asynccontextmanager
            >>> async def lifespan(_: FastAPI) -> None:
            ...     database_manager.initialize()
            ...     yield
            ...     await database_manager.close()
        """
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session = None


# Глобальный менеджер базы данных
database_manager = DatabaseManager(app_settings.DATABASE_URL)
