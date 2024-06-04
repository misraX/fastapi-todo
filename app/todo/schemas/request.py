from pydantic import BaseModel


class TodoRequestSchema(BaseModel):
    title: str
    description: str
