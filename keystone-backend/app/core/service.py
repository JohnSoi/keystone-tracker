from typing import Generic

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from .consts import ServiceOperation
from .database import ModelType
from .typing import DataType, RepositoryType


class BaseService(Generic[RepositoryType, DataType, ModelType]):
    _REPOSITORY: type[RepositoryType]

    def __init__(self, db: AsyncSession, request: Request | None) -> None:
        self._db: AsyncSession = db
        self._request: Request | None = request
        self._repository: RepositoryType = self._REPOSITORY(db)

    async def create(self, payload: DataType) -> ModelType:
        await self._validate_payload(ServiceOperation.CREATE, payload)
        new_entity: ModelType = await self._repository.create(payload.model_dump())
        await self._after_operation(new_entity, payload, ServiceOperation.CREATE)

        return new_entity

    async def update(self, entity_id: int, payload: DataType) -> ModelType:
        await self._validate_payload(ServiceOperation.UPDATE, payload)
        entity: ModelType = await self._repository.update(entity_id, payload.model_dump())
        await self._after_operation(entity, payload, ServiceOperation.UPDATE)

        return entity

    async def delete(self, entity_id: int) -> bool:
        entity: ModelType = await self._repository.get(entity_id)
        await self._validate_payload(ServiceOperation.DELETE, None, entity)
        delete_result: bool = await self._repository.delete(entity_id)
        await self._after_operation(entity, None, ServiceOperation.DELETE)

        return delete_result

    async def _validate_payload(self, operation: ServiceOperation, payload: DataType | None = None, entity: ModelType | None = None) -> None:
        ...

    async def _after_operation(
        self, entity: ModelType, payload: DataType | None, operation: ServiceOperation
    ) -> None: ...
