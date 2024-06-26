"""Adding task completed instead of the status

Revision ID: 62211f0bc128
Revises: f7fbe5fcd6eb
Create Date: 2024-06-05 01:48:30.925698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "62211f0bc128"
down_revision: Union[str, None] = "f7fbe5fcd6eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("task", sa.Column("completed", sa.Boolean(), nullable=True))
    op.drop_index("ix_task_status", table_name="task")
    op.create_index(op.f("ix_task_completed"), "task", ["completed"], unique=False)
    op.drop_column("task", "status")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "task", sa.Column("status", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_index(op.f("ix_task_completed"), table_name="task")
    op.create_index("ix_task_status", "task", ["status"], unique=False)
    op.drop_column("task", "completed")
    # ### end Alembic commands ###
