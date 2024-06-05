from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from app.todo.api import routes as todo_routes
from app.user.auth import fastapi_users, auth_backend
from app.user.schema.request import UserCreateRequestScheme
from app.user.schema.response import UserCreateResponseScheme
from core.exception.handlers import generic_db_error_handler
from core.middleware.sqlalchemy import SQLAlchemyMiddleware

app = FastAPI()


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
app.include_router(todo_routes.router)

app.add_exception_handler(IntegrityError, generic_db_error_handler)

app.add_middleware(SQLAlchemyMiddleware)


@app.get("/health", tags=["health"])
async def read_root():
    return {"message": "Welcome to the Game 🎮!"}
