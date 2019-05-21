"""empty message

Revision ID: 98e80597ce4d
Revises: 
Create Date: 2019-05-10 12:58:42.435949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98e80597ce4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('publishers', sa.Column('operator_licence', sa.String(length=120), nullable=True))
    op.add_column('publishers', sa.Column('reg_certificate', sa.String(length=120), nullable=True))
    op.add_column('publishers', sa.Column('tax_registration', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('publishers', 'tax_registration')
    op.drop_column('publishers', 'reg_certificate')
    op.drop_column('publishers', 'operator_licence')
    # ### end Alembic commands ###