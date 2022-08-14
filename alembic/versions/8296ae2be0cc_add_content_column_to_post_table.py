"""add content column to post table

Revision ID: 8296ae2be0cc
Revises: 86a8d90dee0e
Create Date: 2022-08-14 20:42:46.658960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8296ae2be0cc'
down_revision = '86a8d90dee0e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
