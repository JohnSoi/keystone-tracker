"""Основной модуль приложения."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import AppSettings, get_app_settings
from app.core.database import database_manager, get_db
from app.users import user_routes, UserModel, get_current_user

app_settings: AppSettings = get_app_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> None:
    database_manager.initialize()
    yield
    await database_manager.close()


app: FastAPI = FastAPI(title=app_settings.APP_NAME, version=app_settings.APP_VERSION, lifespan=lifespan)


@app.middleware("http")
async def add_auth_user_data(request: Request, call_next):
    try:
        auth_data = request.headers.get("Authorization")

        if not auth_data:
            return await call_next(request)

        db: AsyncSession = await anext(get_db())
        scheme, credentials = auth_data.split(" ")
        credentials: HTTPAuthorizationCredentials = HTTPAuthorizationCredentials(scheme=scheme, credentials=str(credentials))
        print(credentials)
        user: UserModel = await get_current_user(credentials, db)
        request.state.user = user
    except HTTPException as exc:
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            return await call_next(request)
        else:
            raise exc

    return await call_next(request)


@app.get("/status", tags=["status"])
async def status_page(db_session: AsyncSession = Depends(get_db)):
    """Статус приложения."""

    if not app_settings.DEBUG:
        return {}

    result: dict[str, str] = {
        "app_start": "ok",
    }

    try:
        await db_session.execute(text("SELECT 1"))
        result["database"] = "ok"
    except Exception as exc:
        result["database"] = "fail"
        result["database_error"] = str(exc)

    return result

app.include_router(user_routes)
