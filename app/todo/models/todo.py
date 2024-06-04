from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.db import BaseModel


class Todo(BaseModel):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(GUID, ForeignKey("user.id"))
    title = Column(String, index=True)
    description = Column(Text)

    tasks = relationship("Task", back_populates="todo", cascade="all, delete-orphan")

    owner = relationship("User", back_populates="todos")
