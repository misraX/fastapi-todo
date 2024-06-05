import abc
import uuid
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy import Select, and_, Delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.todo.models import SharedTodo, Todo
from core.db.session import get_async_session


class SharedTodoRepositoryABC(abc.ABC):
    @abc.abstractmethod
    async def share(self, shared_todo: SharedTodo) -> SharedTodo:
        ...

    @abc.abstractmethod
    async def get_shared_todos(
        self, user_id: uuid.UUID, skip: int, limit: int
    ) -> list[SharedTodo]:
        ...

    @abc.abstractmethod
    async def get_shared_todo_by_id(self, todo_id: str, user: uuid.UUID) -> SharedTodo:
        ...

    @abc.abstractmethod
    async def unshare(self, todo_id: str, user_id: uuid.UUID) -> None:
        ...


class SharedTodoRepository(SharedTodoRepositoryABC):
    def __init__(
        self, session: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)
    ) -> None:
        self.session = session

    async def share(self, shared_todo: SharedTodo) -> SharedTodo:
        self.session.add(shared_todo)
        await self.session.commit()
        await self.session.refresh(shared_todo)
        return shared_todo

    async def unshare(self, todo_id: str, user_id: uuid.UUID) -> None:
        statement = Delete(SharedTodo).where(
            and_(SharedTodo.todo_id == todo_id, SharedTodo.user_id == user_id)
        )
        result = await self.session.execute(statement)
        await self.session.commit()
        return result

    async def get_shared_todos(
        self, user_id: uuid.UUID, skip: int, limit: int
    ) -> list[SharedTodo]:
        statement = Select(SharedTodo).where(SharedTodo.user_id == user_id)
        statement = statement.options(
            joinedload(SharedTodo.todo).joinedload(Todo.owner)
        )
        statement = statement.offset(skip).limit(limit)
        results = await self.session.execute(statement)
        results = results.scalars().all()
        return results

    async def get_shared_todo_by_id(self, todo_id, user: uuid.UUID) -> SharedTodo:
        statement = Select(SharedTodo).where(and_(SharedTodo.todo_id == todo_id))
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()
