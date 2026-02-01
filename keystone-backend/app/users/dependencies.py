"""Модуль зависимостей для работы с пользователями."""

from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import AppSettings, get_app_settings
from app.core.database import get_db

from .exceptions import DeletedUserException, InvalidTokenException
from .model import User as UserModel
from .repository import UserRepository

security = HTTPBearer()


settings: AppSettings = get_app_settings()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)
) -> UserModel:
    """
    Зависимость для получения текущего пользователя.

    Args:
        credentials (HTTPAuthorizationCredentials): Данные авторизации.
        db (AsyncSession): Сессия базы данных.

    Returns:
        (UserModel): Текущий пользователь.

    Examples:
        >>> from fastapi import APIRouter
        >>> user_routes = APIRouter()
        >>>
        >>> @user_routes.get("/me", description="Получение данных пользователя")
        >>> async def user_update(user_data: UserModel = Depends(get_current_user)) -> UserModel:
        ...     return user_data
    Raises:
        InvalidTokenException: Если токен невалидный.
        DeletedUserException: Если пользователь удален.
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_uuid: str | None = payload.get("uuid")

        if user_uuid is None:
            raise InvalidTokenException()
    except jwt.PyJWTError as exc:
        raise InvalidTokenException() from exc

    user: UserModel | None = await UserRepository(db).get_by_uuid(UUID(user_uuid))

    if user is None:
        raise InvalidTokenException()

    # Проверяем, активен ли пользователь
    if user.is_deleted:
        raise DeletedUserException()

    return user
