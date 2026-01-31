from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import BaseModel, TimestampMixin, UUIDMixin
from app.users import UserModel


class AccessRestore(BaseModel, UUIDMixin, TimestampMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[UserModel] = relationship(UserModel, lazy="joined", uselist=False, cascade="all, delete")
    used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
