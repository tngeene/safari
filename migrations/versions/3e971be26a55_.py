"""empty message

Revision ID: 3e971be26a55
Revises: a3625aca7a6a
Create Date: 2019-01-18 11:41:15.046047

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3e971be26a55'
down_revision = 'a3625aca7a6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_listings_duration', table_name='listings')
    op.drop_column('listings', 'duration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listings', sa.Column('duration', mysql.VARCHAR(length=120), nullable=True))
    op.create_index('ix_listings_duration', 'listings', ['duration'], unique=False)
    # ### end Alembic commands ###