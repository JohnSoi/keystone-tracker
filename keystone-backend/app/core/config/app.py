"""Модуль конфигурации приложения."""

from datetime import date
from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .validators import validate_app_version


class AppSettings(BaseSettings):
    """
    Основной класс конфигурации приложения.

    Attributes:
        APP_NAME (str): Название приложения.
        APP_VERSION (str): Версия приложения.

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
