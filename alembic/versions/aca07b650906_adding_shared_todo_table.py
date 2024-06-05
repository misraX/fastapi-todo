"""Adding Shared Todo table

Revision ID: aca07b650906
Revises: 6347a4d88e5c
Create Date: 2024-06-04 19:17:04.304286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_users_db_sqlalchemy import GUID

# revision identifiers, used by Alembic.
revision: str = "aca07b650906"
down_revision: Union[str, None] = "6347a4d88e5c"
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
    op.create_index(
        op.f("ix_shared_todo_todo_id"), "shared_todo", ["todo_id"], unique=False
    )
    op.create_index(
        op.f("ix_shared_todo_user_id"), "shared_todo", ["user_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_shared_todo_user_id"), table_name="shared_todo")
    op.drop_index(op.f("ix_shared_todo_todo_id"), table_name="shared_todo")
    op.drop_table("shared_todo")
    # ### end Alembic commands ###
