from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from core.db import BaseModel


class Task(BaseModel):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("todo.id"))
    owner_id = Column(GUID, ForeignKey("user.id"))
    title = Column(String, index=True)
    description = Column(Text)
    priority = Column(Integer, index=True)
    completed = Column(Boolean, default=False, index=True)
    todo = relationship("Todo", back_populates="tasks")
    owner = relationship("User", back_populates="tasks")
