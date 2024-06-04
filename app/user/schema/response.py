from fastapi_users.schemas import BaseUser


class UserCreateRequestScheme(BaseUser):
    username: str
