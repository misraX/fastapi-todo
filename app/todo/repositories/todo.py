import abc
import uuid
from typing import AsyncGenerator
from typing import TypeVar, Type

from fastapi import Depends
from fastapi_users.password import PasswordHelper
from sqlalchemy import Select, and_, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.todo.models import Todo
from core.db import BaseModel
from core.db.session import session_factory, get_async_session

ModelType = TypeVar("ModelType", bound=BaseModel)

password_helper = PasswordHelper()

guinevere_password_hash = password_helper.hash("guinevere")


async def save(model: Type[ModelType]):
    async with session_factory() as async_session:
        async with async_session.begin():
            async_session.add(model)


class TodoRepositoryABC(abc.ABC):
    @abc.abstractmethod
    async def get_todo_by_id(self, todo_id: int, user_id: uuid.UUID) -> Todo | None:
        ...

    @abc.abstractmethod
    async def create_todo(self, todo: Todo) -> Todo | None:
        ...

    @abc.abstractmethod
    async def get_todos(
        self, user_id: uuid.UUID, skip: int, limit: int
    ) -> list[Todo] | None:
        ...

    @abc.abstractmethod
    async def delete_todo_by_id(self, todo_id: int, user_id: uuid.UUID) -> None:
        ...


class TodoRepository(TodoRepositoryABC):
    def __init__(
        self, session: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)
    ) -> None:
        self.session = session

    async def get_todo_by_id(self, todo_id: int, user_id: uuid.UUID) -> Todo | None:
        statement = Select(Todo).where(
            and_(Todo.id == todo_id, Todo.owner_id == user_id)
        )
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()

    async def get_todos(
        self, user_id: uuid.UUID, skip: int, limit: int
    ) -> list[Todo] | None:
        statement = Select(Todo).where(and_(Todo.owner_id == user_id))
        statement = statement.offset(skip).limit(limit)
        results = await self.session.execute(statement)
        return results.scalars().all()

    async def create_todo(self, todo: Todo) -> Todo | None:
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        return todo

    async def delete_todo_by_id(self, todo_id: int, user_id: uuid.UUID) -> None:
        statement = Delete(Todo).where(
            and_(Todo.id == todo_id, Todo.owner_id == user_id)
        )
        result = await self.session.execute(statement)
        await self.session.commit()
        return result
