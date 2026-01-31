"""Модуль базового репозитория."""
from datetime import UTC, datetime
from typing import Generic
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import EntityNotFoundException, EntityNotUUIDException, NotValidUUIDException
from .typing import ModelType


class BaseRepository(Generic[ModelType]):
    """
    Базовый репозиторий. Все репозитории должны наследоваться от него.

    Attributes:
        _session_db (AsyncSession): Сессия базы данных.
        _MODEL (ModelType): Модель базы данных. Является обобщенным типом.
    """

    _MODEL: type[ModelType]

    def __init__(self, session_db: AsyncSession) -> None:
        """
        Инициализация репозитория.

        Args:
            session_db (AsyncSession): Сессия базы данных.
        """
        self._session_db: AsyncSession = session_db

    async def create(self, data: dict) -> ModelType:
        """
        Создание сущности.

        Args:
            data (dict): Данные сущности.

        Returns:
            (ModelType): Данные после создания.

        Examples:
            >>> async def create_user(entity_data: dict) -> ModelType:
            ...     repository = BaseRepository(...)
            ...     # <User id=1, name="John Doe">
            ...     await repository.create(data)
        """
        model: ModelType = self._MODEL()
        await self._before_create(data)
        return await self._save_entity(model, data)

    async def get(self, entity_id: int) -> ModelType:
        """
        Получение сущности по ID.

        Args:
            entity_id (int): ID сущности.

        Returns:
            (ModelType): Данные сущности.

        Examples:
            >>> async def get_user(en_id: int) -> ModelType:
            ...     repository = BaseRepository(...)
            ...     # <User id=1, name="John Doe">
            ...     await repository.get(en_id)
            ...     # raise EntityNotFoundException
            ...     await repository.get(100500)

        Raises:
            EntityNotFoundException: Если сущности не существует.
        """
        entity: ModelType | None = await self._session_db.get(self._MODEL, entity_id)

        if not entity:
            raise EntityNotFoundException(entity_id)

        return entity

    async def get_or_none(self, entity_id: int) -> ModelType | None:
        """
        Получение сущности по ID. Если сущности не существует, вернет None.

        Args:
            entity_id (int): ID сущности.

        Returns:
            (ModelType | None): Данные сущности. None, если сущности не существует.

        Examples:
            >>> async def get_user(en_id: int) -> ModelType | None:
            ...     repository = BaseRepository(...)
            ...     # <User id=1, name="John Doe">
            ...     await repository.get_or_none(en_id)
            ...     # None
            ...     await repository.get_or_none(100500)
        """
        try:
            return await self.get(entity_id)
        except EntityNotFoundException:
            return None

    async def get_by_uuid(self, uuid: UUID) -> ModelType | None:
        """
        Получение сущности по UUID.

        Args:
            uuid (UUID): UUID сущности.

        Returns:
            (ModelType | None): Данные сущности. None, если сущности не существует.

        Examples:
            >>> async def get_by_user_uuid(entity_uuid: UUID) -> ModelType | None:
            ...     repository = BaseRepository(...)
            ...     # <User id=1, name="John Doe">
            ...     await repository.get_by_uuid(UUID("123e4567-e89b-12d3-a456-426614174000"))
            ...     # None
            ...     await repository.get_by_uuid(UUID("123e4567-e89b-12d3-a456-426614174001"))
        Raises:
            NotValidUUIDException: Если UUID не валидный.
            EntityNotUUIDException: Если у сущности нет поля UUID.
        """
        if not isinstance(uuid, UUID):
            raise NotValidUUIDException()

        if not hasattr(self._MODEL, "uuid"):
            raise EntityNotUUIDException()

        data: ModelType | None = await self._session_db.scalar(select(self._MODEL).where(self._MODEL.uuid == uuid))

        if data is None:
            return None

        return data

    async def update(self, entity_id: int, new_data: dict) -> ModelType:
        """
        Обновление сущности.

        Args:
            entity_id (int): ID сущности.
            new_data (dict): Новые данные для обновления.

        Returns:
            (ModelType): Данные после обновления. None, если сущности не существует.
        """
        entity: ModelType = await self.get(entity_id)

        await self._before_update(entity, new_data)

        return await self._save_entity(entity, new_data)

    async def delete(self, entity_id: int) -> bool:
        """
        Удаление сущности. Если у сущности есть поле deleted_at, то оно будет помечено как удаленная.

        Args:
            entity_id (int): ID сущности.

        Returns:
            (bool): True, если сущность удалена.

        Examples:
            >>> async def delete_user(en_id: int) -> None:
            ...     repository = BaseRepository(...)
            ...     # True
            ...     await repository.delete(en_id)
            ...     # False
            ...     await repository.delete(100500)
        """
        entity: ModelType = await self.get(entity_id)

        if hasattr(entity, "deleted_at") and not getattr(entity, "deleted_at"):
            await self.update(entity_id, {"deleted_at": datetime.now(UTC)})
            return True

        await self._session_db.delete(entity)
        return True

    async def _before_create(self, data: dict) -> None:
        """
        Обработчик перед созданием записи.

        Args:
            data (dict): Данные сущности для создания.
        """
        ...

    async def _before_update(self, entity: ModelType, new_data: dict) -> None:
        """
        Обработчик перед обновлением записи.

        Args:
            entity (ModelType): Сущность.
            new_data (dict): Новые данные для обновления
        """
        ...

    async def _save_entity(self, model: ModelType, data: dict) -> ModelType:
        """
        Запись сущности в базу данных.

        Args:
            model (ModelType): Модель сущности.
            data (dict): Данные сущности для записи

        Returns:
            (ModelType): Данные после записи.
        """
        for key, value in data.items():
            if hasattr(model, key):
                setattr(model, key, value)

        self._session_db.add(model)
        await self._session_db.commit()
        await self._session_db.refresh(model)

        return model
