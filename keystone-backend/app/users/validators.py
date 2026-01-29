import re
from datetime import date

from .consts import EMAIL_VALIDATION_EXP, MIN_USER_AGE
from .exceptions import NotValidEmailException, InvalidBirthDateException, FutureBirthDateException, NotAllowedAgeException


def validate_email(email: str) -> str:
    if not email or not isinstance(email, str) or not re.match(EMAIL_VALIDATION_EXP, email):
        raise NotValidEmailException()

    return email


def validate_birth_date(birth_date: date | str) -> date:
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
