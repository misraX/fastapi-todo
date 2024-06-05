from fastapi import APIRouter

from app.todo.api import todo, task, shared_todo

router = APIRouter()
router.include_router(todo.todo_router)
router.include_router(task.task_router)
router.include_router(shared_todo.shared_todo_router)
