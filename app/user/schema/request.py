from typing import Optional

from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr


class UserCreateRequestScheme(CreateUpdateDictModel):
    email: EmailStr
    password: str
    username: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
