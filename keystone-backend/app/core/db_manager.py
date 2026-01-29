from typing import Any, AsyncGenerator

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .config import AppSettings, get_app_settings

app_settings: AppSettings = get_app_settings()


class DatabaseManager:
    def __init__(self, db_url: str | PostgresDsn) -> None:
        self._db_url: str = str(db_url)
        self._engine = None
        self._session = None


    def initialize(self) -> None:
        try:
            self._engine = create_async_engine(
                self._db_url, echo=app_settings.DEBUG,pool_pre_ping=True, pool_recycle=3600
            )
            self._session = async_sessionmaker(
                self._engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False
            )
        except Exception as e:
            raise Exception(f"Failed to initialize database: {e}") from e

    async def get_session(self) -> AsyncGenerator[Any, Any]:
        if self._session is None:
            raise Exception("Database session is not initialized")

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
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session = None

database_manager = DatabaseManager(app_settings.DATABASE_URL)

async def get_db():
    async for session in database_manager.get_session():
        yield session
