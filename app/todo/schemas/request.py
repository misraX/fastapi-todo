from typing import Optional

from pydantic import BaseModel

from app.todo.schemas.common import CommonTodoTasksMixin


class TodoRequestSchema(CommonTodoTasksMixin, BaseModel):
    ...


class TaskRequestSchema(CommonTodoTasksMixin, BaseModel):
    todo_id: int
    priority: Optional[int]
