from typing import Optional

from pydantic import BaseModel, EmailStr

from app.todo.schemas.common import CommonTodoTasksMixin


class TodoRequestSchema(CommonTodoTasksMixin, BaseModel):
    ...


class TaskRequestSchema(CommonTodoTasksMixin, BaseModel):
    todo_id: int
    priority: Optional[int]


class SharedTodoRequestSchema(BaseModel):
    email: EmailStr


class TaskRequestPartialUpdateSchema(BaseModel):
    todo_id: Optional[int] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
    title: Optional[str] = None
    description: Optional[str] = None
