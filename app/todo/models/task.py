from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.db import BaseModel


class Task(BaseModel):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("todo.id"))
    owner_id = Column(GUID, ForeignKey("user.id"))
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, index=True)
    priority = Column(Integer, index=True)

    todo = relationship("Todo", back_populates="tasks")
    owner = relationship("User", back_populates="tasks")
