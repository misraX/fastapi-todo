from fastapi import Depends, HTTPException

from app.todo.models import SharedTodo, Todo, Task
from app.todo.repositories.shared_todo import (
    SharedTodoRepository,
    SharedTodoRepositoryABC,
)
from app.todo.repositories.task import TaskRepository, TaskRepositoryABC
from app.todo.repositories.todo import TodoRepository, TodoRepositoryABC
from app.todo.schemas.request import SharedTodoRequestSchema
from app.user.auth import get_user_manager
from app.user.models.user import UserManager
from test.conftest import User


class SharedTodoService(object):
    def __init__(
        self,
        todo_repository: TodoRepositoryABC = Depends(TodoRepository),
        shared_todo_repository: SharedTodoRepositoryABC = Depends(SharedTodoRepository),
        user_repository: UserManager = Depends(get_user_manager),
        task_repository: TaskRepositoryABC = Depends(TaskRepository),
    ):
        self.todo_repository = todo_repository
        self.user_repository = user_repository
        self.task_repository = task_repository
        self.shared_todo_repository = shared_todo_repository

    async def share(
        self, shared_todo: SharedTodoRequestSchema, todo_id: int, user: User
    ) -> SharedTodo:
        todo: Todo = await self.todo_repository.get_todo_by_id(todo_id, user.id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo does not exist")

        user = await self.user_repository.get_by_email(user_email=shared_todo.email)
        if user is None:
            raise HTTPException(status_code=403, detail="Operation not permitted")

        shared_todo: SharedTodo = SharedTodo()
        shared_todo.user_id = user.id
        shared_todo.todo_id = todo.id
        return await self.shared_todo_repository.share(shared_todo)

    async def unshare(self, todo_id, user):
        """Simpley delete the shared_todo record from the database"""
        return await self.shared_todo_repository.unshare(todo_id, user.id)

    async def get_shared_todos(
        self, user: User, skip: int, limit: int
    ) -> list[SharedTodo]:
        return await self.shared_todo_repository.get_shared_todos(user.id, skip, limit)

    async def get_shared_todo_by_id(
        self, todo_id: int, user: User
    ) -> SharedTodo | None:
        return await self.shared_todo_repository.get_shared_todo_by_id(todo_id, user.id)

    async def get_shared_todo_tasks(
        self, user: User, todo_id, skip: int, limit: int
    ) -> list[Task]:
        shared_todo = await self.shared_todo_repository.get_shared_todo_by_id(
            todo_id, user.id
        )
        if shared_todo is None:
            raise HTTPException(status_code=404, detail="Shared todo not found")
        return await self.task_repository.get_shared_tasks(
            user.id, shared_todo, todo_id, skip, limit
        )
