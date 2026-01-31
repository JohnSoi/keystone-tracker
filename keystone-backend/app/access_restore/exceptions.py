from app.core import BadRequestException


class InvalidRestoreTokenException(BadRequestException):
    _MESSAGE = "Токен восстановления некорректен"


class TokenUsedException(BadRequestException):
    _MESSAGE = "Токен восстановления уже был использован"


class ExpiredRestoreTokenException(BadRequestException):
    _MESSAGE = "Срок действия токена восстановления истек. Пожалуйста, запросите новый токен восстановления."
