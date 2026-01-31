from datetime import UTC, datetime, timedelta
from uuid import UUID

from app.core import BaseService, ServiceOperation
from app.core.database import ModelType

from .consts import EXPIRED_ACCESS_RESTORE_TOKEN_HOURS
from .exceptions import ExpiredRestoreTokenException, InvalidRestoreTokenException, TokenUsedException
from .model import AccessRestore as AccessRestoreModel
from .repositories import AccessRestoreRepository
from .schemas import AccessRestoreData


class AccessRestoreService(BaseService[AccessRestoreRepository, AccessRestoreData, AccessRestoreModel]):
    _REPOSITORY = AccessRestoreRepository

    async def redeem(self, token: UUID) -> int:
        token_data: AccessRestoreModel = await self._repository.get_by_uuid(token)

        if not token_data:
            raise InvalidRestoreTokenException()

        if token_data.used_at:
            raise TokenUsedException()

        current_time: datetime = datetime.now(UTC)
        expired_time: datetime = current_time - timedelta(hours=EXPIRED_ACCESS_RESTORE_TOKEN_HOURS)

        if token_data.created_at < expired_time:
            raise ExpiredRestoreTokenException()

        await self._repository.update(token_data.id, {"used_at": current_time})

        return int(str(token_data.user_id))

    async def _after_operation(self, entity: ModelType, data: AccessRestoreData, operation: ServiceOperation) -> None:
        match operation:
            case ServiceOperation.CREATE:
                # TODO: Отправка письма о восстановлении доступа. Из data брать email и user_deleted
                ...
