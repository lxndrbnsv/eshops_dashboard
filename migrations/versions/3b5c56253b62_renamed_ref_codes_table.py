"""renamed ref_codes table

Revision ID: 3b5c56253b62
Revises: 357d041658d4
Create Date: 2021-06-14 08:05:56.191380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b5c56253b62'
down_revision = '357d041658d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ref_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ref_code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ref_code_id'), 'ref_code', ['id'], unique=False)
    op.drop_index('ix_ref_codes_id', table_name='ref_codes')
    op.drop_table('ref_codes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ref_codes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ref_code', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ref_codes_id', 'ref_codes', ['id'], unique=False)
    op.drop_index(op.f('ix_ref_code_id'), table_name='ref_code')
    op.drop_table('ref_code')
    # ### end Alembic commands ###
