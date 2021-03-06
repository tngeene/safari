"""empty message

Revision ID: f6aa8eb85254
Revises: c09298a93c04
Create Date: 2019-08-07 16:36:41.115506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6aa8eb85254'
down_revision = 'c09298a93c04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('disclaimers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=10000), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('disclaimers')
    # ### end Alembic commands ###
