import pytest
from faker import Faker
from fastapi.testclient import TestClient

faker = Faker()


@pytest.fixture
def test_client():
    from main import app

    client = TestClient(app)
    yield client


@pytest.fixture
async def user_data():
    return {
        "username": faker.user_name(),
        "password": faker.password(),
        "email": faker.email(),
    }


async def test_register_user(user_data, test_client):
    response = test_client.post("/user/register", json=user_data)
    assert response.status_code == 201
    response_data = response.json()
    assert "id" in response_data
