"""Fixing mapping

Revision ID: 182454100c89
Revises: a3817f6ef5e5
Create Date: 2024-06-05 04:11:39.619913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "182454100c89"
down_revision: Union[str, None] = "a3817f6ef5e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "shared_todo",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", GUID(), nullable=False),
        sa.Column("todo_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["todo_id"],
            ["todo.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id", "user_id", "todo_id"),
    )
    op.create_index(op.f("ix_shared_todo_id"), "shared_todo", ["id"], unique=False)
    op.create_index(
        op.f("ix_shared_todo_todo_id"), "shared_todo", ["todo_id"], unique=False
    )
    op.create_index(
        op.f("ix_shared_todo_user_id"), "shared_todo", ["user_id"], unique=False
    )
    op.drop_index("ix_shared_todos_id", table_name="shared_todos")
    op.drop_index("ix_shared_todos_todo_id", table_name="shared_todos")
    op.drop_index("ix_shared_todos_user_id", table_name="shared_todos")
    op.drop_table("shared_todos")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "shared_todos",
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("todo_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["todo_id"], ["todo.id"], name="shared_todos_todo_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name="shared_todos_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", "user_id", "todo_id", name="shared_todos_pkey"),
    )
    op.create_index(
        "ix_shared_todos_user_id", "shared_todos", ["user_id"], unique=False
    )
    op.create_index(
        "ix_shared_todos_todo_id", "shared_todos", ["todo_id"], unique=False
    )
    op.create_index("ix_shared_todos_id", "shared_todos", ["id"], unique=False)
    op.drop_index(op.f("ix_shared_todo_user_id"), table_name="shared_todo")
    op.drop_index(op.f("ix_shared_todo_todo_id"), table_name="shared_todo")
    op.drop_index(op.f("ix_shared_todo_id"), table_name="shared_todo")
    op.drop_table("shared_todo")
    # ### end Alembic commands ###