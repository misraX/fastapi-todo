import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TodoResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    owner_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    owner_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
