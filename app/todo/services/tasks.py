from fastapi import Depends

from app.todo.models import Task
from app.todo.repositories.task import TaskRepository, TaskRepositoryABC
from app.todo.schemas.request import TaskRequestSchema
from app.user.models.user import User
from core.db import unit_of_work


class TaskService(object):
    def __init__(self, task_repository: TaskRepositoryABC = Depends(TaskRepository)):
        self.task_repository = task_repository

    @unit_of_work
    async def create_task(self, request: TaskRequestSchema, user: User) -> Task:
        task = Task(**request.dict())
        task.owner = user
        result = await self.task_repository.create_task(task)
        return result

    async def get_task_by_id(self, todo_id: int, user: User):
        return await self.task_repository.get_task_by_id(todo_id, user.id)

    async def get_tasks(
        self, user: User, skip: int, limit: int, todo_id: int
    ) -> list[Task]:
        return await self.task_repository.get_tasks(user.id, skip, limit, todo_id)

    async def delete_task_by_id(self, todo_id: int, user: User) -> None:
        return await self.task_repository.delete_task_by_id(todo_id, user.id)
