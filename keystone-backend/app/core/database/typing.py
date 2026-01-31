from typing import TypeVar

from app.core.database import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
