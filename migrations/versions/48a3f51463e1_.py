"""empty message

Revision ID: 48a3f51463e1
Revises: 58c8b291562f
Create Date: 2021-06-14 20:25:33.736969

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '48a3f51463e1'
down_revision = '58c8b291562f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_avatar', sa.LargeBinary(), nullable=True))
    op.drop_column('user', 'use_avatar')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('use_avatar', postgresql.BYTEA(), autoincrement=False, nullable=True))
    op.drop_column('user', 'user_avatar')
    # ### end Alembic commands ###
