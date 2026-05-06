"""agregar cantidad a insumos

Revision ID: 4e679de5026f
Revises: 768742ec2187
Create Date: 2026-03-07 19:38:20.366074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e679de5026f'
down_revision = '768742ec2187'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('insumos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cantidad', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    with op.batch_alter_table('insumos', schema=None) as batch_op:
        batch_op.drop_column('cantidad')