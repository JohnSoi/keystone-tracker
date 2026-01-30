"""Модуль для работы с JWT токенами."""

from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer

from .config import AppSettings, get_app_settings

# Схема безопасности для получения токена из запроса
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
# Класс настроек приложения
app_settings: AppSettings = get_app_settings()


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Создание JWT токена.

    Args:
        data (dict): Данные для токена
        expires_delta (timedelta | None): Время жизни токена.

    Returns:
        (str): JWT токен.

    Examples:
        >>> from app.core import create_access_token
        >>> create_access_token({"sub": "1234567890"})
    """
    to_encode: dict = data.copy()
    expire: datetime = datetime.now(UTC) + timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta

    to_encode.update({"exp": expire})

    encoded_jwt: str = jwt.encode(to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    Декодирование JWT токена.

    Args:
        token (str): JWT токен.

    Returns:
        (dict | None): Декодированные данные из токена. Если токен не валидный, то None.

    Examples:
        >>> from app.core import decode_access_token, create_access_token
        >>> test_token = create_access_token({"sub": "1234567890"})
        >>> decode_access_token(test_token) # {"sub": "1234567890"}
    """
    try:
        result: dict = jwt.decode(token, app_settings.SECRET_KEY, algorithms=app_settings.ALGORITHM)
        return result
    except (jwt.ExpiredSignatureError, jwt.PyJWTError):
        return None
