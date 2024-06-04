import dataclasses
import uuid
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Optional,
)

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI, Response
from fastapi_users import exceptions, models, schemas
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy import Strategy
from fastapi_users.db import BaseUserDatabase
from fastapi_users.jwt import SecretType
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.password import PasswordHelper
from pydantic import UUID4, SecretStr
from pytest_mock import MockerFixture

from app.user.models.user import UserManager as BaseUserManager

password_helper = PasswordHelper()

guinevere_password_hash = password_helper.hash("guinevere")
angharad_password_hash = password_helper.hash("angharad")
viviane_password_hash = password_helper.hash("viviane")
lancelot_password_hash = password_helper.hash("lancelot")
excalibur_password_hash = password_helper.hash("excalibur")

IDType = UUID4


@dataclasses.dataclass
class UserModel(models.UserProtocol[IDType]):
    email: str
    username: str
    hashed_password: str
    id: IDType = dataclasses.field(default_factory=uuid.uuid4)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class User(schemas.BaseUser[IDType]):
    ...


class UserCreate(schemas.BaseUserCreate):
    ...


class UserUpdate(schemas.BaseUserUpdate):
    ...


@pytest.fixture(params=["SECRET", SecretStr("SECRET")])
def secret(request) -> SecretType:
    return request.param


@pytest.fixture
def user() -> UserModel:
    return UserModel(
        email="misrax@misrax.com",
        username="misrax",
        hashed_password=guinevere_password_hash,
    )


@pytest.fixture
def inactive_user() -> UserModel:
    return UserModel(
        email="ted@ted.bt",
        username="teddy_bear",
        hashed_password=angharad_password_hash,
        is_active=False,
    )


@pytest.fixture
def verified_user() -> UserModel:
    return UserModel(
        email="lake.lady@camelot.bt",
        username="lake",
        hashed_password=excalibur_password_hash,
        is_active=True,
        is_verified=True,
    )


@pytest.fixture
def superuser() -> UserModel:
    return UserModel(
        email="merlin@camelot.bt",
        username="merlin",
        hashed_password=viviane_password_hash,
        is_superuser=True,
        is_verified=True,
    )


@pytest.fixture
def verified_superuser() -> UserModel:
    return UserModel(
        email="the.real.merlin@camelot.bt",
        username="therealmerlin",
        hashed_password=viviane_password_hash,
        is_superuser=True,
        is_verified=True,
    )


@pytest.fixture
def mock_user_db(
    user: UserModel,
    verified_user: UserModel,
    inactive_user: UserModel,
    superuser: UserModel,
    verified_superuser: UserModel,
) -> BaseUserDatabase[UserModel, IDType]:
    class MockUserDatabase(BaseUserDatabase[UserModel, IDType]):
        async def get(self, id: UUID4) -> Optional[UserModel]:
            if id == user.id:
                return user
            if id == verified_user.id:
                return verified_user
            if id == inactive_user.id:
                return inactive_user
            if id == superuser.id:
                return superuser
            if id == verified_superuser.id:
                return verified_superuser
            return None

        async def get_by_email(self, email: str) -> Optional[UserModel]:
            lower_email = email.lower()
            if lower_email == user.email.lower():
                return user
            if lower_email == verified_user.email.lower():
                return verified_user
            if lower_email == inactive_user.email.lower():
                return inactive_user
            if lower_email == superuser.email.lower():
                return superuser
            if lower_email == verified_superuser.email.lower():
                return verified_superuser
            return None

        async def create(self, create_dict: Dict[str, Any]) -> UserModel:
            return UserModel(**create_dict)

        async def get_by_username(self, username: str) -> Optional[UserModel]:
            if username == user.username:
                return user
            if username == verified_user.username:
                return verified_user
            if username == inactive_user.username:
                return inactive_user
            if username == superuser.username:
                return superuser
            if username == verified_superuser.username:
                return verified_superuser
            return None

        async def update(
            self, user: UserModel, update_dict: Dict[str, Any]
        ) -> UserModel:
            for field, value in update_dict.items():
                setattr(user, field, value)
            return user

        async def delete(self, user: UserModel) -> None:
            pass

    return MockUserDatabase()


@pytest.fixture
def make_user_manager(mocker: MockerFixture):
    def _make_user_manager(user_manager_class, mock_user_db):
        user_manager = user_manager_class(mock_user_db)
        mocker.spy(user_manager, "get_by_email")
        mocker.spy(user_manager, "authenticate")
        mocker.spy(user_manager, "get_by_username")
        mocker.spy(user_manager, "request_verify")
        mocker.spy(user_manager, "verify")
        mocker.spy(user_manager, "forgot_password")
        mocker.spy(user_manager, "reset_password")
        mocker.spy(user_manager, "on_after_register")
        mocker.spy(user_manager, "on_after_request_verify")
        mocker.spy(user_manager, "on_after_verify")
        mocker.spy(user_manager, "on_after_forgot_password")
        mocker.spy(user_manager, "on_after_reset_password")
        mocker.spy(user_manager, "on_after_update")
        mocker.spy(user_manager, "on_before_delete")
        mocker.spy(user_manager, "on_after_delete")
        mocker.spy(user_manager, "on_after_login")
        mocker.spy(user_manager, "_update")
        return user_manager

    return _make_user_manager


@pytest.fixture
def user_manager(make_user_manager, mock_user_db):
    return make_user_manager(BaseUserManager, mock_user_db)


@pytest.fixture
def get_user_manager(user_manager):
    def _get_user_manager():
        return user_manager

    return _get_user_manager


@pytest.fixture
def get_user_manager_oauth(user_manager_oauth):
    def _get_user_manager_oauth():
        return user_manager_oauth

    return _get_user_manager_oauth


class MockTransport(BearerTransport):
    def __init__(self, tokenUrl: str):
        super().__init__(tokenUrl)

    async def get_logout_response(self) -> Any:
        return Response()

    @staticmethod
    def get_openapi_logout_responses_success() -> OpenAPIResponseType:
        return {}


class MockStrategy(Strategy[UserModel, IDType]):
    async def read_token(
        self, token: Optional[str], user_manager
    ) -> Optional[UserModel]:
        if token is not None:
            try:
                parsed_id = user_manager.parse_id(token)
                return await user_manager.get(parsed_id)
            except (exceptions.InvalidID, exceptions.UserNotExists):
                return None
        return None

    async def write_token(self, user: UserModel) -> str:
        return str(user.id)

    async def destroy_token(self, token: str, user: UserModel) -> None:
        return None


def get_mock_authentication(name: str):
    return AuthenticationBackend(
        name=name,
        transport=MockTransport(tokenUrl="/login"),
        get_strategy=lambda: MockStrategy(),
    )


@pytest.fixture
def mock_authentication():
    return get_mock_authentication(name="mock")


@pytest.fixture
def get_test_client():
    async def _get_test_client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, None]:
        async with LifespanManager(app):
            async with httpx.AsyncClient(
                app=app, base_url="http://app.io"
            ) as test_client:
                yield test_client

    return _get_test_client
