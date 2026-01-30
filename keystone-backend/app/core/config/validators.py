"""Модуль валидаторов параметров конфигурации."""

from . import exceptions as exc
from .consts import APP_VERSION_LENGTH, APP_VERSION_PART_DELIMITER, APP_VERSION_PART_LENGTH


def validate_app_version(app_version: str) -> str:
    """
    Валидация версии приложения.

    Args:
        app_version (str): Версия приложения.

    Returns:
        (str): Корректная версия приложения.

    Raises:
        exc.VersionIsNotStringException: Если версия приложения не строка.
        exc.VersionIsNotValidException: Если версия приложения не соответствует формату.
        exc.VersionPartInvalidLengthException: Если длина части версии не равна 2.
        exc.VersionPartIsNotIntegerException: Если составная часть версии не целое число.

    Example:
        >>> validate_app_version("1.0")
        # VersionIsNotValidException - так как версия не соответствует формату 'year.month.patch'
        >>> validate_app_version("1.0.a")
        # VersionPartIsNotIntegerException - так как часть версии не является целым числом
        >>> validate_app_version("1.0.0")
        # "1.0.0" - корректная версия приложения
    """
    if not isinstance(app_version, str):
        raise exc.VersionIsNotStringException()

    if APP_VERSION_PART_DELIMITER not in app_version:
        raise exc.VersionIsNotValidException()

    version_parts: list[str] = app_version.split(APP_VERSION_PART_DELIMITER)

    if len(version_parts) != APP_VERSION_LENGTH:
        raise exc.VersionIsNotValidException()

    if any(len(part) != APP_VERSION_PART_LENGTH for part in version_parts):
        raise exc.VersionPartInvalidLengthException()

    try:
        [int(part) for part in version_parts]
    except ValueError as exception:
        raise exc.VersionPartIsNotIntegerException() from exception

    return app_version
