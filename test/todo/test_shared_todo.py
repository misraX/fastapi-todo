from random import randint
from typing import TypeVar, Type

from fastapi_users.password import PasswordHelper

from app.todo.models import Todo, Task, SharedTodo
from app.user.models.user import User
from core.db import BaseModel
from core.db.session import session_factory

ModelType = TypeVar("ModelType", bound=BaseModel)

password_helper = PasswordHelper()

guinevere_password_hash = password_helper.hash("guinevere")


async def save(model: Type[ModelType]):
    async with session_factory() as async_session:
        async with async_session.begin():
            async_session.add(model)


async def test_create_todo():
    user = User(
        email=f"misrax{randint(1000, 99999)}@misrax",
        hashed_password=guinevere_password_hash,
        username="misrax-{random_number}".format(random_number=randint(1000, 9999)),
    )
    user_2 = User(
        email=f"john{randint(1000, 99999)}@john.com",
        hashed_password=guinevere_password_hash,
        username="john-{random_number}".format(random_number=randint(1000, 9999)),
    )
    todo = Todo(
        title=f"test todo {randint(1000, 99999)}",
        description=f"test todo {randint(1000, 99999)}",
        owner=user,
    )
    task = Task(
        title=f"test task {randint(1000, 99999)}",
        todo=todo,
        owner=user,
        description=f"test task {randint(1000, 99999)}",
    )

    shared_todo = SharedTodo(user=user, todo=todo, id=randint(1000, 9999))
    todo.add_shared_with(shared_todo)
    await save(user)
    await save(user_2)
    await save(todo)
    await save(task)
