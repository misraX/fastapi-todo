import abc
import uuid
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy import Select, and_, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.todo.models import Todo
from core.db.session import get_async_session


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

    @abc.abstractmethod
    async def partial_update(self, todo_id: int, todo: Todo) -> Todo:
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

    async def partial_update(self, todo_id: int, todo: Todo) -> Todo:
        await self.session.commit()
        await self.session.refresh(todo)
        return todo
