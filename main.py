import uuid

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi_users.schemas import BaseUser, BaseUserCreate

from app.todo.api import routes as todo_routes
from app.user.api import routes as user_routes
from app.user.models.user import get_user_db, UserManager, User
from core.settings.config import settings

SECRET = settings.secret_key


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(todo_routes.router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/user",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(BaseUser, BaseUserCreate),
    prefix="/user",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(BaseUser),
    prefix="/user",
    tags=["auth"],
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application"}
