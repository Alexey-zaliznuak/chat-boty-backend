"""empty message

Revision ID: b7e9928372f1
Revises: 9c51a9dc7085
Create Date: 2024-09-13 22:34:05.191502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7e9928372f1'
down_revision: Union[str, None] = '9c51a9dc7085'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cases', 'preview_file_id',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('cases', 'preview_og_file_id',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cases', 'preview_og_file_id',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('cases', 'preview_file_id',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###