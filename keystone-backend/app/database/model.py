from sqlalchemy import Integer
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, declarative_base


class CustomModel:
    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


BaseModel = declarative_base(cls=CustomModel)
