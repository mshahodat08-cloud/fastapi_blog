"""add_phone_to_users

Revision ID: 8186c31459a5
Revises: c371d278cc19
Create Date: 2026-05-06 17:38:51.741986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8186c31459a5'
down_revision: Union[str, Sequence[str], None] = 'c371d278cc19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('phone', sa.String(20), nullable=True)
    )
    # Index ham qo'shamiz:
    op.create_index(
        'ix_users_phone',
        'users',
        ['phone'],
        unique=False
    )

def downgrade() -> None:
    op.drop_index('ix_users_phone', table_name='users')
    op.drop_column('users', 'phone')