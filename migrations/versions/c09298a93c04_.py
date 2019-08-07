"""empty message

Revision ID: c09298a93c04
Revises: e2e4bf507364
Create Date: 2019-08-07 15:41:20.459304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c09298a93c04'
down_revision = 'e2e4bf507364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('publishers', sa.Column('director', sa.String(length=120), nullable=True))
    op.add_column('publishers', sa.Column('director_email', sa.String(length=120), nullable=True))
    op.add_column('publishers', sa.Column('director_phone', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('publishers', 'director_phone')
    op.drop_column('publishers', 'director_email')
    op.drop_column('publishers', 'director')
    # ### end Alembic commands ###
