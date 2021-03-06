"""RefCodes table

Revision ID: 357d041658d4
Revises: 45b5a2d6cda9
Create Date: 2021-06-14 07:55:07.063386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '357d041658d4'
down_revision = '45b5a2d6cda9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ref_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ref_code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ref_codes_id'), 'ref_codes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ref_codes_id'), table_name='ref_codes')
    op.drop_table('ref_codes')
    # ### end Alembic commands ###
