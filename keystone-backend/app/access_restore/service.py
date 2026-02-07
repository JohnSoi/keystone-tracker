"""Модуль сервиса восстановления доступа."""

from datetime import UTC, datetime, timedelta
from uuid import UUID

from app.core import BaseService, ServiceOperation
from app.core.database import DataModel
from app.users.repository import UserRepository
from app.worker.tasks import send_access_restore_email

from .consts import EXPIRED_ACCESS_RESTORE_TOKEN_HOURS
from .exceptions import ExpiredRestoreTokenException, InvalidRestoreTokenException, TokenUsedException
from .model import AccessRestore as AccessRestoreModel
from .repositories import AccessRestoreRepository
from .schemas import AccessRestoreData


class AccessRestoreService(BaseService[AccessRestoreRepository, AccessRestoreData, AccessRestoreModel]):
    """Сервис восстановления доступа."""

    _REPOSITORY = AccessRestoreRepository

    async def redeem(self, token: UUID) -> int:
        """
        Метод для восстановления доступа путем погашения токена.

        Args:
            token (UUID): Токен доступа.

        Returns:
            (int): ID пользователя токена.

        Examples:
            >>> async def restore_access(ex_token: UUID) -> int:
            ...     return await AccessRestoreService().redeem(ex_token)

        Raises:
            ExpiredRestoreTokenException: Токен доступа истек.
            InvalidRestoreTokenException: Невалидный токен доступа.
            TokenUsedException: Токен доступа уже использован.
        """
        token_data: AccessRestoreModel | None = await self._repository.get_by_uuid(token)

        if not token_data:
            raise InvalidRestoreTokenException()

        if token_data.is_used:
            raise TokenUsedException()

        current_time: datetime = datetime.now(UTC)
        expired_time: datetime = current_time - timedelta(hours=EXPIRED_ACCESS_RESTORE_TOKEN_HOURS)

        if token_data.created_at < expired_time:
            raise ExpiredRestoreTokenException()

        await self._repository.update(token_data.id, {"used_at": current_time})

        return int(str(token_data.user_id))

    async def _after_operation(
        self, entity: DataModel, _: AccessRestoreData | None, operation: ServiceOperation
    ) -> None:
        """Метод обработки после операций."""
        match operation:
            case ServiceOperation.CREATE:
                user_data = await UserRepository(self._db).get(entity.user_id)
                send_access_restore_email.delay(
                    user_full_name=user_data.full_name, user_email=user_data.email, token=entity.uuid
                )
