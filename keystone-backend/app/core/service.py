# pylint: disable=unnecessary-ellipsis, unused-argument
"""Модуль базового сервиса."""

from typing import Generic

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from .consts import ServiceOperation
from .database.typing import DataModel
from .typing import InputData, Repository


class BaseService(Generic[Repository, InputData, DataModel]):
    """
    Базовый сервис. Все сервисы должны наследоваться от него.

    Attributes:
        _REPOSITORY (type[RepositoryType]): Репозиторий для работы с базой данных.
        _db (AsyncSession): Сессия подключения к базе данных.
        _request (Request | None): Объект запрос, если он был передан.
        _repository (RepositoryType): Репозиторий для работы с базой данных.

    Generic Parameters:
        RepositoryType: Тип репозитория для работы с базой данных.
        DataType: Тип данных для создания/обновления сущности.
        ModelType: Тип модели сущности.
    """

    _REPOSITORY: type[Repository]

    def __init__(self, db: AsyncSession, request: Request | None = None) -> None:
        """
        Инициализация сервиса.

        Args:
            db (AsyncSession): Сессия подключения к базе данных.
            request (Request | None): Объект запрос, если он был передан.
        """
        self._db: AsyncSession = db
        self._request: Request | None = request
        self._repository: Repository = self._REPOSITORY(db)

    async def create(self, payload: InputData) -> DataModel:
        """
        Создание сущности.

        Args:
            payload (DataType): Данные для создания сущности.

        Returns:
            (ModelType): Созданная сущность.

        Examples:
            >>> class UserService(BaseService[Repository, InputData, DataModel]):
            ...     async def create_user(self, data: InputData) -> DataModel:
            ...         return await self.create(payload)
        """
        await self._validate_payload(ServiceOperation.CREATE, payload)
        new_entity: DataModel = await self._repository.create(payload.model_dump())
        await self._after_operation(new_entity, payload, ServiceOperation.CREATE)

        return new_entity

    async def update(self, entity_id: int, payload: InputData) -> DataModel:
        """
        Обновление сущности.

        Args:
            entity_id (int): Идентификатор сущности.
            payload (DataType): Данные для обновления сущности.

        Returns:
            (ModelType): Обновленная сущность.

        Examples:
            >>> class UserService(BaseService[Repository, InputData, DataModel]):
            ...     async def update_user(self, user_id: int, new_data: InputData) -> DataModel:
            ...         return await self.update(user_id, new_data)
        """
        await self._validate_payload(ServiceOperation.UPDATE, payload)
        entity: DataModel = await self._repository.update(entity_id, payload.model_dump())
        await self._after_operation(entity, payload, ServiceOperation.UPDATE)

        return entity

    async def delete(self, entity_id: int) -> bool:
        """
        Удаление сущности.

        Args:
            entity_id (int): Идентификатор сущности.

        Returns:
            (bool): Результат удаления.

        Examples:
            >>> class UserService(BaseService[Repository, InputData, DataModel]):
            ...     async def delete_user(self, user_id: int) -> bool:
            ...         return await self.delete(user_id)
        """
        entity: DataModel = await self._repository.get(entity_id)
        await self._validate_payload(ServiceOperation.DELETE, None, entity)
        delete_result: bool = await self._repository.delete(entity_id)
        await self._after_operation(entity, None, ServiceOperation.DELETE)

        return delete_result

    async def _validate_payload(
        self, operation: ServiceOperation, payload: InputData | None = None, entity: DataModel | None = None
    ) -> None:
        """
        Валидация данных перед выполнением операции.

        Args:
            operation (ServiceOperation): Тип операции.
            payload (DataType | None): Данные для создания/обновления сущности.
            entity (ModelType | None): Сущность для валидации.
        """
        ...

    async def _after_operation(self, entity: DataModel, payload: InputData | None, operation: ServiceOperation) -> None:
        """
        Действия после выполнения операции.

        Args:
            entity (ModelType): Сущность.
            payload (DataType | None): Данные для создания/обновления сущности.
            operation (ServiceOperation): Тип операции.
        """
