from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import LoginConflictException, EmailConflictException, LoginNotFoundException, \
    PasswordIncorrectException
from .repository import UserRepository
from .schemas import UserRegisterData, UserAccessData, UserAuthResponseData
from ..core import verify_password, create_access_token


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self._repository = UserRepository(db)

    async def register(self, payload: UserRegisterData) -> dict | None:
        await self._validate_payload(payload)
        return await self._repository.create(payload.model_dump())

    async def login(self, payload: UserAccessData) -> UserAuthResponseData:
        user: dict = await self._repository.get_by_login(payload.login)

        if not user:
            raise LoginNotFoundException(payload.login)

        if not verify_password(payload.password, user.get("password")):
            raise PasswordIncorrectException()

        return UserAuthResponseData(access_token=create_access_token({"uuid": str(user.get("uuid"))}), refresh_token="123")


    async def _validate_payload(self, payload: UserRegisterData) -> None:
        login: str = payload.login

        if await self._repository.get_by_login(login):
            raise LoginConflictException(login)

        if await self._repository.get_by_email(payload.email):
            raise EmailConflictException(payload.email)
