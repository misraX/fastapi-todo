import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import BaseModel
from core.db.session import get_async_session
from core.settings.config import settings

SECRET = settings.secret_key


class User(SQLAlchemyBaseUserTableUUID, BaseModel):
    ...


async def get_user_db(async_session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(async_session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
