from typing import List

from fastapi import Depends, APIRouter

from app.todo.schemas.response import SharedTodoResponse, TaskResponseSchema
from app.todo.services.shared_todo import SharedTodoService
from app.user.auth import current_user
from app.user.models.user import User

shared_todo_router = APIRouter(prefix="/shared-todo", tags=["shared-todo"])


@shared_todo_router.get("/", response_model=List[SharedTodoResponse])
async def shared_todo(
    shared_todo_service: SharedTodoService = Depends(SharedTodoService),
    user: User = Depends(current_user),
    skip: int = 0,
    limit: int = 100,
):
    result = await shared_todo_service.get_shared_todos(user, skip, limit)
    return result


@shared_todo_router.get("/{todo_id}/tasks", response_model=list[TaskResponseSchema])
async def shared_tasks(
    todo_id: int,
    user: User = Depends(current_user),
    skip: int = 0,
    limit: int = 100,
    shared_todo_service: SharedTodoService = Depends(SharedTodoService),
):
    return await shared_todo_service.get_shared_todo_tasks(user, todo_id, skip, limit)
