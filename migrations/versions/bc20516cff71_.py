"""empty message

Revision ID: bc20516cff71
Revises: c145bd21d28e
Create Date: 2021-06-11 00:19:11.699747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc20516cff71'
down_revision = 'c145bd21d28e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comment_body_key', 'comment', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('comment_body_key', 'comment', ['body'])
    # ### end Alembic commands ###
