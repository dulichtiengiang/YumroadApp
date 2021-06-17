"""add product price and image

Revision ID: 2587cfb81ee5
Revises: 60493a478fb4
Create Date: 2021-06-15 22:18:50.321756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2587cfb81ee5'
down_revision = '60493a478fb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price_cents', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('picture_url', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('picture_url')
        batch_op.drop_column('price_cents')

    # ### end Alembic commands ###