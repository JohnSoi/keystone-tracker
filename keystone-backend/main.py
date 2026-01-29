"""Основной модуль приложения."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import AppSettings, get_app_settings
from app.core import database_manager, DatabaseManager, get_db

app_settings: AppSettings = get_app_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> None:
    database_manager.initialize()
    yield
    await database_manager.close()


app: FastAPI = FastAPI(title=app_settings.APP_NAME, version=app_settings.APP_VERSION, lifespan=lifespan)


@app.get("/status", tags=["status"])
async def status_page(db_session: AsyncSession = Depends(get_db)):
    """Статус приложения."""

    if not app_settings.DEBUG:
        return {}

    result: dict[str, str] = {
        "app_start": "ok",
        "database_url": str(app_settings.DATABASE_URL)
    }

    try:
        await db_session.execute(text("SELECT 1"))
        result["database"] = "ok"
    except Exception as exc:
        result["database"] = "fail"
        result["database_error"] = str(exc)

    return result
