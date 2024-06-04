from fastapi_users.schemas import BaseUser


class UserCreateResponseScheme(BaseUser):
    username: str
