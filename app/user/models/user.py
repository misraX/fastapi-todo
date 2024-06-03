from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import BaseModel, session


class User(SQLAlchemyBaseUserTable, BaseModel):
    ...


async def get_user_db(async_session: AsyncSession = Depends(session)):
    yield SQLAlchemyUserDatabase(async_session, User)
