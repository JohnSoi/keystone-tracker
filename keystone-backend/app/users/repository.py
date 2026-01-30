from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import User as UserModel
from ..core import hash_password


class UserRepository:
    def __init__(self, session_db: AsyncSession) -> None:
        self._session_db: AsyncSession = session_db

    async def create(self, data: dict) -> dict:
        model: UserModel = UserModel()

        data["password"] = hash_password(data.get("password"))

        for key, value in data.items():
            if hasattr(model, key):
                setattr(model, key, value)

        self._session_db.add(model)
        await self._session_db.commit()
        await self._session_db.refresh(model)

        return model.to_dict()

    async def get_by_login(self, login: str) -> dict | None:
        user_data: UserModel | None = await self._session_db.scalar(
            select(UserModel).where(UserModel.login == login)
        )

        if not user_data:
            return None

        return user_data.to_dict()

    async def get_by_email(self, email: str) -> dict | None:
        user_data: UserModel | None = await self._session_db.scalar(
            select(UserModel).where(UserModel.email == email)
        )

        if not user_data:
            return None

        return user_data.to_dict()
