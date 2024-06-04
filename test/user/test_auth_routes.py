from typing import Any, AsyncGenerator, Dict, Tuple, cast

import httpx
import pytest
from fastapi import FastAPI, status
from fastapi_users.authentication import Authenticator
from fastapi_users.router import ErrorCode, get_auth_router

from test.conftest import UserModel


@pytest.fixture
def app_factory(get_user_manager, mock_authentication):
    def _app_factory(requires_verification: bool) -> FastAPI:
        authenticator = Authenticator([mock_authentication], get_user_manager)

        mock_auth_router = get_auth_router(
            mock_authentication,
            get_user_manager,
            authenticator,
            requires_verification=requires_verification,
        )

        app = FastAPI()
        app.include_router(mock_auth_router, prefix="/mock")

        return app

    return _app_factory


@pytest.fixture(
    params=[True, False], ids=["required_verification", "not_required_verification"]
)
async def test_app_client(
    request, get_test_client, app_factory
) -> AsyncGenerator[Tuple[httpx.AsyncClient, bool], None]:
    requires_verification = request.param
    app = app_factory(requires_verification)

    async for client in get_test_client(app):
        yield client, requires_verification


@pytest.mark.unittest
@pytest.mark.parametrize("path", ["/mock/login"])
class TestLogin:
    async def test_empty_body(
        self,
        path,
        test_app_client: Tuple[httpx.AsyncClient, bool],
        user_manager,
    ):
        client, _ = test_app_client
        response = await client.post(path, data={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert user_manager.on_after_login.called is False

    async def test_missing_username(
        self,
        path,
        test_app_client: Tuple[httpx.AsyncClient, bool],
        user_manager,
    ):
        client, _ = test_app_client
        data = {"password": "guinevere"}
        response = await client.post(path, data=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert user_manager.on_after_login.called is False

    async def test_missing_password(
        self,
        path,
        test_app_client: Tuple[httpx.AsyncClient, bool],
        user_manager,
    ):
        client, _ = test_app_client
        data = {"username": "king"}
        response = await client.post(path, data=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert user_manager.on_after_login.called is False

    async def test_not_existing_user(
        self,
        path,
        test_app_client: Tuple[httpx.AsyncClient, bool],
        user_manager,
    ):
        client, _ = test_app_client
        data = {"username": "lancelot@camelot.bt", "password": "guinevere"}
        response = await client.post(path, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = cast(Dict[str, Any], response.json())
        assert data["detail"] == ErrorCode.LOGIN_BAD_CREDENTIALS
        assert user_manager.on_after_login.called is False

    async def test_wrong_password(
        self,
        path,
        test_app_client: Tuple[httpx.AsyncClient, bool],
        user_manager,
    ):
        client, _ = test_app_client
        data = {"username": "king.arthur@camelot.bt", "password": "percival"}
        response = await client.post(path, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = cast(Dict[str, Any], response.json())
        assert data["detail"] == ErrorCode.LOGIN_BAD_CREDENTIALS
        assert user_manager.on_after_login.called is False

    @pytest.mark.parametrize("username", ["lake", "lake"])
    async def test_valid_credentials_verified(
        self,
        path,
        username,
        test_app_client: Tuple[httpx.AsyncClient, bool],
        user_manager,
        verified_user: UserModel,
    ):
        client, _ = test_app_client
        data = {
            "username": username,
            "password": "excalibur",
            "scope": "",
            "client_id": "",
            "client_secret": "",
            "grant_type": "",
        }
        response = await client.post(path, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "access_token": str(verified_user.id),
            "token_type": "bearer",
        }
        assert user_manager.on_after_login.called is True
        args, kwargs = user_manager.on_after_login.call_args
        assert len(args) == 3
        assert all(x is not None for x in args)

    async def test_inactive_user(
        self,
        path,
        test_app_client: Tuple[httpx.AsyncClient, bool],
        user_manager,
    ):
        client, _ = test_app_client
        data = {
            "username": "teddy_bear",
            "password": "excalibur",
            "scope": "",
            "client_id": "",
            "client_secret": "",
            "grant_type": "",
        }
        response = await client.post(path, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = cast(Dict[str, Any], response.json())
        assert data["detail"] == ErrorCode.LOGIN_BAD_CREDENTIALS
        assert user_manager.on_after_login.called is False


@pytest.mark.unittest
@pytest.mark.parametrize("path", ["/mock/logout"])
class TestLogout:
    async def test_missing_token(
        self,
        path,
        test_app_client: Tuple[httpx.AsyncClient, bool],
    ):
        client, _ = test_app_client
        response = await client.post(path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_valid_credentials_unverified(
        self,
        path,
        test_app_client: Tuple[httpx.AsyncClient, bool],
        user: UserModel,
    ):
        client, requires_verification = test_app_client
        response = await client.post(
            path, headers={"Authorization": f"Bearer {user.id}"}
        )
        if requires_verification:
            assert response.status_code == status.HTTP_403_FORBIDDEN
        else:
            assert response.status_code == status.HTTP_200_OK

    async def test_valid_credentials_verified(
        self,
        path,
        test_app_client: Tuple[httpx.AsyncClient, bool],
        verified_user: UserModel,
    ):
        client, _ = test_app_client
        response = await client.post(
            path, headers={"Authorization": f"Bearer {verified_user.id}"}
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.unittest
async def test_route_names(app_factory, mock_authentication):
    app = app_factory(False)
    login_route_name = f"auth:{mock_authentication.name}.login"
    assert app.url_path_for(login_route_name) == "/mock/login"

    logout_route_name = f"auth:{mock_authentication.name}.logout"
    assert app.url_path_for(logout_route_name) == "/mock/logout"
