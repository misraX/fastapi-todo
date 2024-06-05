from typing import List

from fastapi import Depends, APIRouter

from app.todo.schemas.request import SharedTodoRequestSchema
from app.todo.schemas.response import TodoResponseSchema
from app.todo.services.shared_todo import SharedTodoService
from app.todo.services.todo import TodoRequestSchema, TodoService
from app.user.auth import current_user
from app.user.models.user import User

todo_router = APIRouter(prefix="/todo", tags=["todo"])


@todo_router.post("/", response_model=TodoResponseSchema)
async def create_todo(
    todo: TodoRequestSchema,
    todo_service: TodoService = Depends(TodoService),
    user: User = Depends(current_user),
):
    todo = await todo_service.create_todo(todo, user=user)
    return todo


@todo_router.get("/{todo_id}")
async def get_todo(
    todo_id: int,
    user: User = Depends(current_user),
    todo_service: TodoService = Depends(TodoService),
):
    """Get a todo item by todo_id"""
    return await todo_service.get_todo_by_id(todo_id, user)


@todo_router.get("/", response_model=List[TodoResponseSchema])
async def get_todos(
    user: User = Depends(current_user),
    todo_service: TodoService = Depends(TodoService),
    skip: int = 0,
    limit: int = 100,
):
    """Get all todos related to the current user, this endpoint support infinite scrolling"""
    todos = await todo_service.get_todos(user, skip, limit)
    return todos


@todo_router.delete("/{todo_id}", status_code=204, response_model=None)
async def delete_todo(
    todo_id: int,
    user: User = Depends(current_user),
    todo_service: TodoService = Depends(TodoService),
):
    """Deleting an existing todo, this will delete only the user's todo."""
    return await todo_service.delete_todo_by_id(todo_id, user)


@todo_router.post("/{todo_id}/share/")
async def share_todo(
    shared_todo: SharedTodoRequestSchema,
    todo_id: int,
    shared_todo_service: SharedTodoService = Depends(SharedTodoService),
    user: User = Depends(current_user),
):
    return await shared_todo_service.share(shared_todo, todo_id, user)


@todo_router.delete("/{todo_id}/unshare/", status_code=204, response_model=None)
async def unshare_todo(
    todo_id: int,
    shared_todo_service: SharedTodoService = Depends(SharedTodoService),
    user: User = Depends(current_user),
):
    return await shared_todo_service.unshare(todo_id, user)
