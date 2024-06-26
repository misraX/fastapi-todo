from fastapi import Depends, HTTPException

from app.todo.models import Todo
from app.todo.repositories.todo import TodoRepository, TodoRepositoryABC
from app.todo.schemas.request import TodoRequestSchema, TodoRequestPartialSchema
from app.user.models.user import User
from core.db import unit_of_work


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
        result = await self.todo_repository.get_todo_by_id(todo_id, user.id)
        if not result:
            raise HTTPException(404, detail="Todo does not exist")

    async def get_todos(self, user: User, skip: int, limit: int) -> list[Todo]:
        return await self.todo_repository.get_todos(user.id, skip, limit)

    async def delete_todo_by_id(self, todo_id: int, user: User) -> None:
        return await self.todo_repository.delete_todo_by_id(todo_id, user.id)

    async def partial_update(
        self, todo_id: int, todo: TodoRequestPartialSchema, user: User
    ):
        todo_item: Todo = await self.todo_repository.get_todo_by_id(todo_id, user.id)
        if todo_item is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        update_data = todo.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo_item, key, value)
        return await self.todo_repository.partial_update(todo_id, todo_item)
