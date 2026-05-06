"""agrega stock_minimo a insumos

Revision ID: 1e60d302573b
Revises: d2cbdadb49ce
Create Date: 2026-03-25 10:13:08.865351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e60d302573b'
down_revision = 'd2cbdadb49ce'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('insumos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stock_minimo', sa.Integer(), nullable=False, server_default='5'))


def downgrade():
    with op.batch_alter_table('insumos', schema=None) as batch_op:
        batch_op.drop_column('stock_minimo')