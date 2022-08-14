"""add last few columns to post table

Revision ID: 33e551845d3f
Revises: d621e3f6b33d
Create Date: 2022-08-14 21:05:16.328251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33e551845d3f'
down_revision = 'd621e3f6b33d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts",'created_at')
    pass
