"""Модуль исключений при работе с БД."""
from uuid import UUID

from app.core import BaseHttpException, NotFoundException, NotValidEntityException


class SessionNotCreatedException(BaseHttpException):
    """Исключение, возникающее при отсутствии сессии."""

    _MESSAGE = "Сессия для подключения к БД не создана"


class NotValidUUIDException(NotValidEntityException):
    """Исключение, возникающее при невалидном UUID."""

    _MESSAGE = "Невалидный UUID для получения сущности."


class EntityNotUUIDException(BaseHttpException):
    """Исключение, возникающее при отсутствии UUID у сущности."""

    _MESSAGE = "Данный объект не имеет поле UUID."


class EntityNotFoundException(NotFoundException):
    def __init__(self, entity_id: int) -> None:
        super().__init__(f"Сущность с id {entity_id} не найдена")


class EntityNotFoundByUUIDException(NotFoundException):
    def __init__(self, entity_uuid: UUID) -> None:
        super().__init__(f"Сущность с uuid {entity_uuid} не найдена")
