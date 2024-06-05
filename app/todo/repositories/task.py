import abc
import uuid
from typing import AsyncGenerator, Optional

from fastapi import Depends
from sqlalchemy import Select, and_, Delete, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.todo.models import Task, SharedTodo
from core.db.session import get_async_session


class TaskRepositoryABC(abc.ABC):
    @abc.abstractmethod
    async def get_task_by_id(self, task_id: int, user_id: uuid.UUID) -> Task | None:
        ...

    @abc.abstractmethod
    async def create_task(self, task: Task) -> Task | None:
        ...

    @abc.abstractmethod
    async def get_tasks(
        self,
        user_id: uuid.UUID,
        skip: int,
        limit: int,
        todo_id: Optional[int] = None,
        order_by=asc(Task.created_at),
    ) -> list[Task] | None:
        ...

    @abc.abstractmethod
    async def delete_task_by_id(self, task_id: int, user_id: uuid.UUID) -> None:
        ...

    @abc.abstractmethod
    async def partial_update(self, task_id: int, task: Task) -> Task:
        ...

    @abc.abstractmethod
    async def get_shared_tasks(
        self,
        user_id: uuid.UUID,
        shared_todo: SharedTodo,
        todo_id: int,
        skip: int,
        limit: int,
        order_by=asc(Task.created_at),
    ):
        pass


class TaskRepository(TaskRepositoryABC):
    def __init__(
        self, session: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)
    ) -> None:
        self.session = session

    async def get_task_by_id(self, task_id: int, user_id: uuid.UUID) -> Task | None:
        statement = Select(Task).where(
            and_(Task.id == task_id, Task.owner_id == user_id)
        )
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()

    async def create_task(self, task: Task) -> Task | None:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_shared_tasks(
        self,
        user_id: uuid.UUID,
        shared_todo: SharedTodo,
        todo_id: int,
        skip: int,
        limit: int,
        order_by=asc(Task.created_at),
    ):
        statement = Select(Task)
        statement = statement.order_by(asc(Task.priority), asc(Task.created_at))
        if todo_id is not None:
            statement = statement.where(and_(Task.todo_id == todo_id))
        statement = statement.offset(skip).limit(limit)
        print(statement)
        results = await self.session.execute(statement)
        results = results.scalars().all()
        return results

    async def get_tasks(
        self,
        user_id: uuid.UUID,
        skip: int,
        limit: int,
        todo_id: Optional[int] = None,
        order_by=asc(Task.created_at),
    ) -> list[Task] | None:
        statement = Select(Task).where(Task.owner_id == user_id)
        statement = statement.order_by(asc(Task.priority), asc(Task.created_at))
        if todo_id is not None:
            statement = statement.where(and_(Task.todo_id == todo_id))
        statement = statement.offset(skip).limit(limit)
        results = await self.session.execute(statement)
        return results.scalars().all()

    async def delete_task_by_id(self, task_id: int, user_id: uuid.UUID) -> None:
        statement = Delete(Task).where(
            and_(Task.id == task_id, Task.owner_id == user_id)
        )
        result = await self.session.execute(statement)
        await self.session.commit()
        return result

    async def partial_update(self, task_id: int, task: Task) -> Task:
        await self.session.commit()
        await self.session.refresh(task)
        return task
