from datetime import date

import pytest

from app.users.exceptions import (
    FutureBirthDateException,
    InvalidBirthDateException,
    NotAllowedAgeException,
    NotValidEmailException,
)
from app.users.validators import (
    validate_birth_date,
    validate_email,
)


def test_validate_email_valid():
    """Тест валидации валидного email."""
    assert validate_email("test@test.com") == "test@test.com"
    assert validate_email("user.name@domain.org") == "user.name@domain.org"
    assert validate_email("test123@sub.domain.com") == "test123@sub.domain.com"


def test_validate_email_invalid():
    """Тест валидации невалидного email."""
    invalid_emails = [
        "invalid-email",
        "@test.com",
        "test@",
        "test.com",
        "",
        None,
        123,
    ]

    for email in invalid_emails:
        with pytest.raises(NotValidEmailException):
            validate_email(email)


def test_validate_email_edge_cases():
    """Тест граничных случаев для валидации email."""
    # Проверяем строку вместо email
    with pytest.raises(NotValidEmailException):
        validate_email("not_an_email")

    # Проверяем пустую строку
    with pytest.raises(NotValidEmailException):
        validate_email("")

    # Проверяем некорректный тип
    with pytest.raises(NotValidEmailException):
        validate_email(123)


def test_validate_birth_date_valid():
    """Тест валидации валидной даты рождения."""
    # Дата рождения 25 лет назад
    test_date = date.today().replace(year=date.today().year - 25)
    assert validate_birth_date(test_date) == test_date


def test_validate_birth_date_string_type():
    """Тест проверки типа аргумента."""
    with pytest.raises(InvalidBirthDateException):
        validate_birth_date("2000-01-01")


def test_validate_birth_date_invalid_type():
    """Тест валидации с некорректным типом аргумента."""
    invalid_values = [None, "", 123, "not_a_date"]

    for value in invalid_values:
        with pytest.raises(InvalidBirthDateException):
            validate_birth_date(value)


def test_validate_birth_date_future_date():
    """Тест валидации даты рождения в будущем."""
    future_date = date.today().replace(year=date.today().year + 1)
    with pytest.raises(FutureBirthDateException):
        validate_birth_date(future_date)


def test_validate_birth_date_too_young():
    """Тест валидации возраста меньше 18 лет."""
    # Дата рождения 17 лет назад
    too_young_date = date.today().replace(year=date.today().year - 17)
    with pytest.raises(NotAllowedAgeException):
        validate_birth_date(too_young_date)


def test_validate_birth_date_exactly_18_years():
    """Тест валидации возраста ровно 18 лет."""
    today = date.today()
    # Если сегодня 29 февраля, а 18 лет назад был високосный год
    try:
        eighteen_years_ago = today.replace(year=today.year - 18)
        assert validate_birth_date(eighteen_years_ago) == eighteen_years_ago
    except ValueError:
        # Обработка случая 29 февраля
        eighteen_years_ago = date(today.year - 18, 2, 28)
        assert validate_birth_date(eighteen_years_ago) == eighteen_years_ago


def test_validate_birth_date_past_date():
    """Тест валидации даты рождения в прошлом более чем на 18 лет."""
    # Дата рождения 30 лет назад
    past_date = date.today().replace(year=date.today().year - 30)
    assert validate_birth_date(past_date) == past_date
