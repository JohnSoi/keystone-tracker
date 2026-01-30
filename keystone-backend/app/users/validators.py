"""Модуль валидаторов для работы с пользователями."""

import re
from datetime import date

from .consts import EMAIL_VALIDATION_EXP, MIN_USER_AGE
from .exceptions import (
    FutureBirthDateException,
    InvalidBirthDateException,
    NotAllowedAgeException,
    NotValidEmailException,
)


def validate_email(email: str) -> str:
    """
    Валидация email.

    Args:
        email (str): Указанный email.

    Returns:
        (str): Валидированный email.

    Examples:
        >>> validate_email("test@test.com") # True
        >>> validate_email("test") # False

    Raises:
        NotValidEmailException: Если email не валиден.
    """
    if not email or not isinstance(email, str) or not re.match(EMAIL_VALIDATION_EXP, email):
        raise NotValidEmailException()

    return email


def validate_birth_date(birth_date: date | str) -> date:
    """
    Валидация даты рождения.

    Args:
        birth_date (date | str): Указанная дата рождения.

    Returns:
        (date): Валидированная дата рождения.

    Examples:
        >>> validate_birth_date("1990-01-01") # True
        >>> validate_birth_date("test") # False

    Raises:
        InvalidBirthDateException: Если дата не валидна.
        FutureBirthDateException: Если дата в будущем.
        NotAllowedAgeException: Если пользователю меньше 18 лет.
    """
    if not birth_date or not isinstance(birth_date, date):
        raise InvalidBirthDateException()

    # Проверяем, что дата не в будущем
    today = date.today()
    if birth_date > today:
        raise FutureBirthDateException()

    # Проверяем, что пользователю больше 18 лет
    eighteen_years_ago = today.replace(year=today.year - MIN_USER_AGE)
    if birth_date > eighteen_years_ago:
        raise NotAllowedAgeException()

    return birth_date
