"""Модуль конфигурации приложения."""

from datetime import date
from functools import lru_cache

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

from .validators import validate_app_version


class AppSettings(BaseSettings):
    """
    Основной класс конфигурации приложения.

    Attributes:
        APP_NAME (str): Название приложения.
        APP_VERSION (str): Версия приложения.

        DEBUG (bool): Флаг режима отладки.

        SECRET_KEY (str): Секретный ключ для шифрования токенов.
            Используется для подписи JWT токенов.
        ALGORITHM (str): Алгоритм шифрования токенов.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Время жизни токена в минутах.

        DATABASE_HOST (str): Хост базы данных.
        DATABASE_PORT (int): Порт базы данных.
        DATABASE_NAME (str): Название базы данных.
        DATABASE_USER (str): Имя пользователя базы данных.
        DATABASE_PASSWORD (str): Пароль пользователя базы данных.

    Examples:
        >>> # Создание кешируемой функции получения настроек приложения
        >>> @lru_cache()
        >>>
        >>> def get_app_settings_cache() -> AppSettings:
        ...     return AppSettings()
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=True)

    APP_NAME: str = "KeyStone API"
    APP_VERSION: str = ""

    DEBUG: bool = False

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "keystone_db"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_URL: PostgresDsn | str = ""

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @field_validator("APP_VERSION", mode="before")
    @classmethod
    def validate_version(cls, value: str | None) -> str:
        """
        Устанавливает текущую версию приложения, если она не задана.

        Args:
            value (str): версия приложения

        Returns:
            (str): Текущая версия приложения.
        """
        if value:
            return value

        current_data: date = date.today()
        return f"{str(current_data.year)[2:]}.{current_data.month:02d}.00"

    @field_validator("APP_VERSION", mode="after")
    @classmethod
    def validate_version_format(cls, value: str) -> str:
        """
        Валидирует формат версии приложения.

        Args:
            value (str): Версия приложения.

        Returns:
            (str): Корректная версия приложения.
        """
        return validate_app_version(value)

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def create_database_url(cls, value: PostgresDsn | None, values: ValidationInfo) -> PostgresDsn:
        """
        Создает URL базы данных, если он не задан в настройках.

        Args:
            value (PostgresDsn | None): URL базы данных.
            values (ValidationInfo): Значения других полей конфигурации.

        Returns:
            (PostgresDsn): URL базы данных.
        """
        if value:
            return value

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=values.data.get("DATABASE_HOST"),
            port=values.data.get("DATABASE_PORT"),
            username=values.data.get("DATABASE_USER"),
            password=values.data.get("DATABASE_PASSWORD"),
            path=values.data.get("DATABASE_NAME"),
        )


@lru_cache()
def get_app_settings() -> AppSettings:
    """
    Возвращает настройки приложения.

    Notes:
        - Используется кэширование для оптимизации производительности.

    Returns:
        (AppSettings): Настройки приложения.

    Examples:
        >>> from app.core.config import get_app_settings, AppSettings
        >>>
        >>> settings: AppSettings = get_app_settings()
        >>> print(settings.APP_NAME)  # Выводит название приложения
        >>> print(settings.APP_VERSION)  # Выводит версию приложения
    """
    return AppSettings()
