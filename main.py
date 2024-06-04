import uuid

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from app.todo.api import routes as todo_routes
from app.todo.repos.task import TaskRepository
from app.user.models.user import get_user_db, UserManager, User
from app.user.schema.request import UserCreateRequestScheme
from app.user.schema.response import UserCreateResponseScheme
from core.settings.config import settings

SECRET = settings.secret_key


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="user/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

app = FastAPI()

app.include_router(todo_routes.router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/user",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(
        UserCreateResponseScheme, UserCreateRequestScheme
    ),
    prefix="/user",
    tags=["auth"],
)


@app.get("/")
async def read_root(task_repo=Depends(TaskRepository)):
    tasks = await task_repo.get_tasks()
    tasks = [task.username for task in tasks if tasks]
    return {"message": f"Welcome to the FastAPI application {tasks}"}
