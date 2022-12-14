"""auto-vote

Revision ID: 906e845279e8
Revises: 795c2e185507
Create Date: 2022-08-14 21:39:20.053334

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '906e845279e8'
down_revision = '795c2e185507'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # # ### commands auto generated by Alembic - please adjust! ###
    # # op.create_table('user',
    # # sa.Column('id', sa.Integer(), nullable=False),
    # # sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    # # sa.Column('email', sa.String(), nullable=False),
    # # sa.Column('password', sa.String(), nullable=True),
    # # sa.PrimaryKeyConstraint('id'),
    # # sa.UniqueConstraint('email')
    # # )
    # op.drop_table('users')
    # op.drop_constraint('post_users_fkey', 'posts', type_='foreignkey')
    # op.create_foreign_key(None, 'posts', 'user', ['owner_id'], ['id'], ondelete='CASCADE')
    # op.drop_constraint('votes_user_id_fkey', 'votes', type_='foreignkey')
    # op.create_foreign_key(None, 'votes', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # --
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )
    
    
    
    # ### end Alembic commands ###


def downgrade() -> None:
    # # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'votes', type_='foreignkey')
    # op.create_foreign_key('votes_user_id_fkey', 'votes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # op.drop_constraint(None, 'posts', type_='foreignkey')
    # op.create_foreign_key('post_users_fkey', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    # op.create_table('users',
    # sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    # sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    # sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    # sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    # sa.PrimaryKeyConstraint('id', name='users_pkey'),
    # sa.UniqueConstraint('email', name='users_email_key')
    # )
    # op.drop_table('votes')
    # ### end Alembic commands ###
    op.drop_table('votes')
 