"""Add slug

Revision ID: 60c057bbede6
Revises: 6ad1760ee48f
Create Date: 2024-08-09 18:46:34.407024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60c057bbede6'
down_revision: Union[str, None] = '6ad1760ee48f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'posts',
        sa.Column(
            'slug',
            sa.String(length=150),
            server_default=sa.text('substring(md5(random()::text), 1, 8)'),
            nullable=False,
        )
    )
    op.add_column('posts', sa.Column('content_file', sa.String(), nullable=True))
    op.add_column('posts', sa.Column('preview_file', sa.String(), nullable=True))
    op.create_index(op.f('ix_posts_slug'), 'posts', ['slug'], unique=True)
    op.drop_column('posts', 'file')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('file', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_posts_slug'), table_name='posts')
    op.drop_column('posts', 'preview_file')
    op.drop_column('posts', 'content_file')
    op.drop_column('posts', 'slug')
    # ### end Alembic commands ###
