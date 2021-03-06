"""empty message

Revision ID: 58c8b291562f
Revises: fc25f3f00b49
Create Date: 2021-06-14 20:23:04.580426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58c8b291562f'
down_revision = 'fc25f3f00b49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('use_avatar', sa.LargeBinary(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'use_avatar')
    # ### end Alembic commands ###
