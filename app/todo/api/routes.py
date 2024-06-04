from fastapi import APIRouter

from app.todo.api import todo, task

router = APIRouter()
router.include_router(todo.todo_router)
router.include_router(task.task_router)
