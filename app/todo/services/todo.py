from fastapi import APIRouter
from fastapi import Depends

from app.todo.models import Todo
from app.todo.repositories.todo import TodoRepository, TodoRepositoryABC
from app.todo.schemas.request import TodoRequestSchema
from app.user.models.user import User
from core.db import unit_of_work

router = APIRouter(prefix="/todo", tags=["todo"])


class TodoService(object):
    def __init__(self, todo_repository: TodoRepositoryABC = Depends(TodoRepository)):
        self.todo_repository = todo_repository

    @unit_of_work
    async def create_todo(self, request: TodoRequestSchema, user: User) -> Todo:
        todo = Todo(**request.dict())
        todo.owner = user
        result = await self.todo_repository.create_todo(todo)
        return result

    async def get_todo_by_id(self, todo_id: int, user: User):
        return await self.todo_repository.get_todo_by_id(todo_id, user.id)

    async def get_todos(self, user: User, skip: int, limit: int) -> list[Todo]:
        return await self.todo_repository.get_todos(user.id, skip, limit)
