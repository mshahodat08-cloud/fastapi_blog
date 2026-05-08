"""add_categories_table_and_relation

Revision ID: b240d1509f26
Revises: 381c171802c3
Create Date: 2026-05-06 17:54:10.938732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'b240d1509f26'
down_revision: Union[str, Sequence[str], None] = '381c171802c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('categories', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_constraint(op.f('posts_category_id_fkey'), 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'categories', ['category_id'], ['id'], ondelete='SET NULL')
    op.drop_index(op.f('ix_users_phone'), table_name='users')



def downgrade() -> None:
    """Downgrade schema."""
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=False)
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key(op.f('posts_category_id_fkey'), 'posts', 'categories', ['category_id'], ['id'])
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.alter_column('categories', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
  
