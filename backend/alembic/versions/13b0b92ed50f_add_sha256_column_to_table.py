"""Add sha256 column to table

Revision ID: 13b0b92ed50f
Revises: 228c47a30cd6
Create Date: 2025-02-19 12:30:49.749283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13b0b92ed50f'
down_revision = '228c47a30cd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('script_flow', sa.Column('sha256', sa.LargeBinary, nullable=True))


def downgrade() -> None:
    op.drop_column('script_flow', 'sha256')
