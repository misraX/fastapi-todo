import uuid
from typing import Optional, Union

from fastapi import Depends
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, UUIDIDMixin, InvalidPasswordException
from fastapi_users import exceptions, models, schemas
from fastapi_users.models import UP
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy import Column
from sqlalchemy import String, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

import app.todo.models as reload_related_models  # noqa
from app.user.schema.request import UserCreateRequestScheme
from core.db import BaseModel
from core.db.session import get_async_session
from core.settings.config import settings

SECRET = settings.secret_key


class User(SQLAlchemyBaseUserTableUUID, BaseModel):
    username = Column(String, unique=True)
    todos = relationship("Todo", back_populates="owner")
    tasks = relationship("Task", back_populates="owner")

    associated_todos = relationship("Todo", secondary="shared_todo", viewonly=True)


class UserDB(SQLAlchemyUserDatabase):
    async def get_by_username(self, username: str) -> Optional[UP]:
        statement = select(self.user_table).where(self.user_table.username == username)
        return await self._get_user(statement)


async def get_user_db(async_session: AsyncSession = Depends(get_async_session)):
    yield UserDB(async_session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    def __init__(self, user_db: SQLAlchemyUserDatabase = UserDB):
        super().__init__(user_db=user_db)

    async def get_by_username(self, username: str) -> models.UP:
        """
        Get a user by username.

        :param username: username of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get_by_username(username)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_username(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        try:
            created_user = await self.user_db.create(user_dict)
            await self.on_after_register(created_user, request)

            return created_user
        except IntegrityError:
            raise exceptions.UserAlreadyExists()

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        """
        Authenticate and return a user following an email and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreateRequestScheme, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")
