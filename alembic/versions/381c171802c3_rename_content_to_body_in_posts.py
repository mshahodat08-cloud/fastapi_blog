"""rename_content_to_body_in_posts

Revision ID: 381c171802c3
Revises: 8186c31459a5
Create Date: 2026-05-06 17:41:44.217105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '381c171802c3'
down_revision: Union[str, Sequence[str], None] = '8186c31459a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'posts',
        'content',      # Eski nom
        new_column_name='body'   # Yangi nom
    )

def downgrade() -> None:
    op.alter_column(
        'posts',
        'body',
        new_column_name='content'
    )
