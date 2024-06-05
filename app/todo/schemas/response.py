import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserEmail(BaseModel):
    email: str


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
    created_at: datetime
    updated_at: datetime
    todo_id: int
    priority: Optional[int] = None
    completed: Optional[bool] = None


class SharedTodoUserResponseSchema(BaseModel):
    email: str


class SharedTodoResponseSchema(BaseModel):
    title: str
    description: str
    owner_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
    owner: SharedTodoUserResponseSchema


class SharedTodoResponse(BaseModel):
    todo: SharedTodoResponseSchema
    todo_id: int
