from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import ForeignKey, Column, Integer, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from core.db import BaseModel


class SharedTodo(BaseModel):
    __tablename__ = "shared_todo"

    __table_args__ = (UniqueConstraint("user_id", "todo_id"),)

    user_id = Column(GUID, ForeignKey("user.id"), primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("todo.id"), primary_key=True, index=True)

    user = relationship(
        "User", backref=backref("shared_todos", cascade="all, delete-orphan")
    )
    todo = relationship(
        "Todo", backref=backref("shared_todos", cascade="all, delete-orphan")
    )
