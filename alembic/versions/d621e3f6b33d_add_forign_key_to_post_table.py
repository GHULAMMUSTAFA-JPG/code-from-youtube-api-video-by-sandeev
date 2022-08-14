"""add forign-key to post table

Revision ID: d621e3f6b33d
Revises: 10e445f573cf
Create Date: 2022-08-14 20:55:52.629976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd621e3f6b33d'
down_revision = '10e445f573cf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fkey',source_table="posts",referent_table="users",
    local_cols=["owner_id"],remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
