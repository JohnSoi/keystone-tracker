import pytest

from app.core.config import exceptions as exc
from app.core.config import validators


def test_validate_app_version_valid():
    """Тест валидной версии приложения."""
    assert validators.validate_app_version("24.01.01") == "24.01.01"
    assert validators.validate_app_version("99.12.31") == "99.12.31"


def test_validate_app_version_not_string():
    """Тест, когда версия приложения не является строкой."""
    with pytest.raises(exc.VersionIsNotStringException):
        validators.validate_app_version(123)
    with pytest.raises(exc.VersionIsNotStringException):
        validators.validate_app_version(None)
    with pytest.raises(exc.VersionIsNotStringException):
        validators.validate_app_version(1.0)


def test_validate_app_version_invalid_format():
    """Тест, когда версия приложения не соответствует формату."""
    with pytest.raises(exc.VersionIsNotValidException):
        validators.validate_app_version("24.01")
    with pytest.raises(exc.VersionIsNotValidException):
        validators.validate_app_version("24-01-01")
    with pytest.raises(exc.VersionIsNotValidException):
        validators.validate_app_version("24.01.01.01")
    with pytest.raises(exc.VersionIsNotValidException):
        validators.validate_app_version("")


def test_validate_app_version_invalid_part_length():
    """Тест, когда длина части версии не равна 2."""
    with pytest.raises(exc.VersionPartInvalidLengthException):
        validators.validate_app_version("2.01.01")
    with pytest.raises(exc.VersionPartInvalidLengthException):
        validators.validate_app_version("24.1.01")
    with pytest.raises(exc.VersionPartInvalidLengthException):
        validators.validate_app_version("24.01.1")
    with pytest.raises(exc.VersionPartInvalidLengthException):
        validators.validate_app_version("24.01.001")


def test_validate_app_version_non_integer_part():
    """Тест, когда часть версии не является целым числом."""
    with pytest.raises(exc.VersionPartIsNotIntegerException):
        validators.validate_app_version("24.01.a1")
    with pytest.raises(exc.VersionPartIsNotIntegerException):
        validators.validate_app_version("24.a1.01")
    with pytest.raises(exc.VersionPartIsNotIntegerException):
        validators.validate_app_version("a4.01.01")
    with pytest.raises(exc.VersionPartIsNotIntegerException):
        validators.validate_app_version("24.01.0a")
