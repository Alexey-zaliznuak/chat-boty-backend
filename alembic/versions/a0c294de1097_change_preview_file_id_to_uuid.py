"""Change preview_file_id to UUID

Revision ID: a0c294de1097
Revises: b7e9928372f1
Create Date: 2024-09-14 21:22:45.249954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0c294de1097'
down_revision: Union[str, None] = 'b7e9928372f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Очистка невалидных UUID в таблице `posts`
    op.execute("""
        UPDATE posts
        SET preview_file_id = NULL
        WHERE preview_file_id IS NOT NULL
        AND NOT preview_file_id ~* '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$';
    """)
    op.execute("""
        UPDATE posts
        SET preview_og_file_id = NULL
        WHERE preview_og_file_id IS NOT NULL
        AND NOT preview_og_file_id ~* '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$';
    """)

    # Очистка невалидных UUID в таблице `cases`
    op.execute("""
        UPDATE cases
        SET preview_file_id = NULL
        WHERE preview_file_id IS NOT NULL
        AND NOT preview_file_id ~* '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$';
    """)
    op.execute("""
        UPDATE cases
        SET preview_og_file_id = NULL
        WHERE preview_og_file_id IS NOT NULL
        AND NOT preview_og_file_id ~* '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$';
    """)

    # Явное указание на преобразование в UUID с использованием выражения USING
    op.execute("""
        ALTER TABLE cases
        ALTER COLUMN preview_file_id TYPE UUID
        USING CASE
            WHEN preview_file_id ~* '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            THEN preview_file_id::uuid
            ELSE NULL
        END;
    """)
    op.execute("""
        ALTER TABLE cases
        ALTER COLUMN preview_og_file_id TYPE UUID
        USING CASE
            WHEN preview_og_file_id ~* '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            THEN preview_og_file_id::uuid
            ELSE NULL
        END;
    """)
    op.execute("""
        ALTER TABLE posts
        ALTER COLUMN preview_file_id TYPE UUID
        USING CASE
            WHEN preview_file_id ~* '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            THEN preview_file_id::uuid
            ELSE NULL
        END;
    """)
    op.execute("""
        ALTER TABLE posts
        ALTER COLUMN preview_og_file_id TYPE UUID
        USING CASE
            WHEN preview_og_file_id ~* '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            THEN preview_og_file_id::uuid
            ELSE NULL
        END;
    """)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'preview_og_file_id',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    op.alter_column('posts', 'preview_file_id',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    op.alter_column('cases', 'preview_og_file_id',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    op.alter_column('cases', 'preview_file_id',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###
