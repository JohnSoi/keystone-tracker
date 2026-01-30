from fastapi import HTTPException, status


class BaseHttpException(HTTPException):
    _STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _MESSAGE: str = "Внутренняя ошибка сервера"

    def __init__(self, message: str | None = None, status_code: int | None = None) -> None:
        super().__init__(detail=message or self._MESSAGE, status_code=status_code or self._STATUS_CODE)

class NotValidEntityException(BaseHttpException):
    _STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    _MESSAGE = "Некорректные данные в запросе"


class EntityConflictException(BaseHttpException):
    _STATUS_CODE = status.HTTP_409_CONFLICT
    _MESSAGE = "Запись уже существует"
