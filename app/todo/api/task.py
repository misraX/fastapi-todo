from typing import Optional

from fastapi import Depends, APIRouter

from app.todo.schemas.request import TaskRequestSchema, TaskRequestPartialUpdateSchema
from app.todo.schemas.response import TaskResponseSchema
from app.todo.services.tasks import TaskService
from app.user.auth import current_user
from app.user.models.user import User

task_router = APIRouter(prefix="/task", tags=["task"])


@task_router.post("/", response_model=TaskResponseSchema)
async def create_task(
    task: TaskRequestSchema,
    task_service: TaskService = Depends(TaskService),
    user: User = Depends(current_user),
):
    task = await task_service.create_task(task, user=user)
    return task


@task_router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_task(
    task_id: int,
    user: User = Depends(current_user),
    task_service: TaskService = Depends(TaskService),
):
    """Get a task item by task_id"""
    return await task_service.get_task_by_id(task_id, user)


@task_router.get("/", response_model=list[TaskResponseSchema])
async def get_tasks(
    todo_id: Optional[int] = None,
    user: User = Depends(current_user),
    task_service: TaskService = Depends(TaskService),
    skip: int = 0,
    limit: int = 100,
):
    """Get all tasks related to the current user, this endpoint support infinite scrolling and filter by todo_id"""
    tasks = await task_service.get_tasks(user, skip, limit, todo_id)
    return tasks


@task_router.delete("/{task_id}", status_code=204, response_model=None)
async def delete_task(
    task_id: int,
    user: User = Depends(current_user),
    task_service: TaskService = Depends(TaskService),
):
    """Deleting an existing task, this will delete only the user's task."""
    return await task_service.delete_task_by_id(task_id, user)


@task_router.patch("/{task_id}", response_model=TaskResponseSchema)
async def partial_update(
    task_id: int,
    task: TaskRequestPartialUpdateSchema,
    user: User = Depends(current_user),
    task_service: TaskService = Depends(TaskService),
):
    """Update an existing task, this will update the user's task. partially update the given fields"""
    return await task_service.partial_update(task_id, task, user)
