from fastapi_users.schemas import CreateUpdateDictModel

from pydantic import EmailStr


class UserCreateRequestScheme(CreateUpdateDictModel):
    email: EmailStr
    password: str
    username: str
