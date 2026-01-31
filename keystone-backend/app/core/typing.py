from typing import TypeVar

from pydantic import BaseModel

from app.core.database import BaseRepository

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)
DataType = TypeVar("DataType", bound=BaseModel)
