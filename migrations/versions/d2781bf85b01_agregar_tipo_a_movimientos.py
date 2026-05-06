"""agregar tipo a movimientos

Revision ID: d2781bf85b01
Revises: c59a3f3c2dca
Create Date: 2026-03-09 11:47:32.393033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2781bf85b01'
down_revision = 'c59a3f3c2dca'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('movimientos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo', sa.String(length=20), nullable=False, server_default='salida'))


def downgrade():
    with op.batch_alter_table('movimientos', schema=None) as batch_op:
        batch_op.drop_column('tipo')