"""Fixing mapping

Revision ID: 29c1e3e6409d
Revises: 182454100c89
Create Date: 2024-06-05 04:17:43.288494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "29c1e3e6409d"
down_revision: Union[str, None] = "182454100c89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_shared_todo_id", table_name="shared_todo")
    op.drop_column("shared_todo", "id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "shared_todo",
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_index("ix_shared_todo_id", "shared_todo", ["id"], unique=False)
    # ### end Alembic commands ###