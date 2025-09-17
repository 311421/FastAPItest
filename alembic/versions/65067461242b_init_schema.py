"""init schema

Revision ID: 65067461242b
Revises: 
Create Date: 2025-09-17 11:58:04.105050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65067461242b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create wallets table (initial schema)
    op.create_table(
        'wallets',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('amount', sa.Numeric(precision=18, scale=2), nullable=False, server_default='0')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('wallets')
