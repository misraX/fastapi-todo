import uuid
from typing import Optional

from pydantic import BaseModel


class TodoResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    owner_id: Optional[uuid.UUID]
