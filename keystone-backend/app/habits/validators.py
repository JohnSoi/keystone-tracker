import re

from .consts import COLOR_REGEX, COLOR_START_WITH, WeekDay, DAYS_IN_WEEK
from .exceptions import InvalidColorTypeException, InvalidColorValueException, InvalidDayInWeekException, \
    TooManyDaysOfWeekException, InvalidDayOfWeekException, DuplicatesInDayOfWeekException


def validate_hex_color(color: str) -> str:
    if not isinstance(color, str):
        raise InvalidColorTypeException()
    
    cleaned_color = color.lstrip(COLOR_START_WITH)
    
    if not re.match(COLOR_REGEX, cleaned_color):
        raise InvalidColorValueException(color)
    
    return f"{COLOR_START_WITH}{cleaned_color.upper()}"


def validate_days_of_week(days: list[int]) -> list[int]:
    if not isinstance(days, list):
        raise InvalidDayOfWeekException()

    if len(days) != len(set(days)):
        raise DuplicatesInDayOfWeekException()

    for day in days:
        if day not in WeekDay.__members__.values():
            raise InvalidDayInWeekException(day)

    if len(days) > DAYS_IN_WEEK:
        raise TooManyDaysOfWeekException()

    return days