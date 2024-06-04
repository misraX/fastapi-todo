from typing import List

from fastapi import Depends, APIRouter

from app.todo.schemas.response import TodoResponseSchema
from app.todo.services.todo import TodoRequestSchema, TodoService
from app.user.auth import current_user
from app.user.models.user import User

router = APIRouter(prefix="/todo", tags=["todo"])


@router.post("/", response_model=TodoResponseSchema)
async def create_todo(
    todo: TodoRequestSchema,
    todo_service: TodoService = Depends(TodoService),
    user: User = Depends(current_user),
):
    todo = await todo_service.create_todo(todo, user=user)
    return todo


@router.get("/{todo_id}")
async def get_todo(
    todo_id: int,
    user: User = Depends(current_user),
    todo_service: TodoService = Depends(TodoService),
):
    return await todo_service.get_todo_by_id(todo_id, user)


@router.get("/", response_model=List[TodoResponseSchema])
async def get_todos(
    user: User = Depends(current_user),
    todo_service: TodoService = Depends(TodoService),
    skip: int = 0,
    limit: int = 100,
):
    todos = await todo_service.get_todos(user, skip, limit)
    return todos
