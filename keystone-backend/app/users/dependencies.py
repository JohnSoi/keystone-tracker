from uuid import UUID

import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_app_settings, AppSettings
from app.core.database import get_db
from .exceptions import InvalidTokenException, DeletedUserException
from .repository import UserRepository
from .model import User as UserModel

security = HTTPBearer()


settings: AppSettings = get_app_settings()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> UserModel:
    """Зависимость для получения текущего пользователя из JWT токена"""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_uuid: str | None = payload.get("uuid")
        if user_uuid is None:
            raise InvalidTokenException()
    except jwt.PyJWTError:
        raise InvalidTokenException()

    user: UserModel = await UserRepository(db).get_by_uuid(UUID(user_uuid))

    if user is None:
        raise InvalidTokenException()

    # Проверяем, активен ли пользователь
    if user.deleted_at:
        raise DeletedUserException()

    return user