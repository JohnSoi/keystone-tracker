"""Модуль исключений при работе с конфигурацией приложения."""


class VersionIsNotStringException(ValueError):
    """Исключение при попытке передать не строку в качестве версии приложения."""

    def __init__(self) -> None:
        super().__init__("Версия приложения должна быть строкой")


class VersionIsNotValidException(ValueError):
    """Исключение при попытке передать не валидную версию приложения."""

    def __init__(self) -> None:
        super().__init__("Версия приложения должна быть в формате 'year.month.patch'")


class VersionPartInvalidLengthException(ValueError):
    """Исключение при попытке передать не валидную составную часть версии приложения."""

    def __init__(self) -> None:
        super().__init__("Составные части версии должны быть в формате '00'")


class VersionPartIsNotIntegerException(ValueError):
    """Исключение при попытке передать не целое число в качестве составной части версии приложения."""

    def __init__(self) -> None:
        super().__init__("Составные части версии должны быть целыми числами")
