"""empty message

Revision ID: 702a4bd9a4f5
Revises: c1bbcf94306a
Create Date: 2021-06-18 18:16:40.611691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '702a4bd9a4f5'
down_revision = 'c1bbcf94306a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
