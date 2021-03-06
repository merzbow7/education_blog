"""empty message

Revision ID: c145bd21d28e
Revises: 6e7c9c07ef25
Create Date: 2021-06-11 00:10:28.883696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c145bd21d28e'
down_revision = '6e7c9c07ef25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_body_key', 'post', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('post_body_key', 'post', ['body'])
    # ### end Alembic commands ###
