from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import LoginConflictException, EmailConflictException
from .repository import UserRepository
from .schemas import UserRegisterData


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self._repository = UserRepository(db)

    async def register(self, payload: UserRegisterData) -> dict | None:
        await self._validate_payload(payload)
        return await self._repository.create(payload.model_dump())

    async def _validate_payload(self, payload: UserRegisterData) -> None:
        login: str = payload.login

        if await self._repository.get_by_login(login):
            raise LoginConflictException(login)

        if await self._repository.get_by_email(payload.email):
            raise EmailConflictException(payload.email)
