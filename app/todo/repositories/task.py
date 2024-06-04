from sqlalchemy import select

from app.user.models.user import User
from core.db.session import session_factory


class TaskRepository:
    async def get_tasks(self, skip: int = 0, limit: int = 10):
        query = select(User).offset(skip).limit(limit)
        async with session_factory() as read_session:
            result = await read_session.execute(query)
        return result.scalars().all()

    async def create_task(self):
        ...
