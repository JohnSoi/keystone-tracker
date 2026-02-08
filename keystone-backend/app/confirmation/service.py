"""Модуль сервиса подтверждения."""

from datetime import UTC, datetime, timedelta
from uuid import UUID

from app.core import BaseService, ServiceOperation
from app.core.database import DataModel
from app.users.repository import UserRepository
from app.worker import send_confirmation_email

from .consts import EXPIRED_CONFIRM_TOKEN_DAYS
from .exceptions import ExpiredConfirmationTokenException, InvalidConfirmTokenException, TokenUsedException
from .model import Confirmation as ConfirmationModel
from .repository import ConfirmationRepository
from .schemas import ConfirmationData


class ConfirmService(BaseService[ConfirmationRepository, ConfirmationData, ConfirmationModel]):
    """Сервис подтверждения."""

    _REPOSITORY = ConfirmationRepository

    async def redeem(self, token: UUID) -> int:
        """
        Метод для подтверждения путем погашения токена.

        Args:
            token (UUID): Токен доступа.

        Returns:
            (int): ID пользователя токена.

        Examples:
            >>> async def confirm_email(ex_token: UUID) -> int:
            ...     return await ConfirmService().redeem(ex_token)

        Raises:
            InvalidConfirmTokenException: Некорректный токен подтверждения.
            TokenUsedException: Токен подтверждения уже использован.
            ExpiredConfirmationTokenException: Токен подтверждения истек.
        """
        token_data: ConfirmationModel | None = await self._repository.get_by_uuid(token)

        if not token_data:
            raise InvalidConfirmTokenException()

        if token_data.is_used:
            raise TokenUsedException()

        current_time: datetime = datetime.now(UTC)
        expired_time: datetime = current_time - timedelta(days=EXPIRED_CONFIRM_TOKEN_DAYS)

        if token_data.created_at < expired_time:
            raise ExpiredConfirmationTokenException()

        user_id: int = int(str(token_data.user_id))

        await self._repository.update(user_id, {"used_at": current_time})

        return user_id

    async def _after_operation(
        self, entity: DataModel, _: ConfirmationData | None, operation: ServiceOperation
    ) -> None:
        """Метод обработки после операций."""
        match operation:
            case ServiceOperation.CREATE:
                user_data = await UserRepository(self._db).get(entity.user_id)
                send_confirmation_email.delay(
                    token=entity.uuid, user_full_name=user_data.full_name, user_email=user_data.email
                )
