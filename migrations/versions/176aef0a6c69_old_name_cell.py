"""old_name cell

Revision ID: 176aef0a6c69
Revises: 4231210fe803
Create Date: 2021-04-05 17:56:18.976772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '176aef0a6c69'
down_revision = '4231210fe803'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('beauty_services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service', sa.String(length=512), nullable=True),
    sa.Column('description', sa.String(length=1512), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.Column('old_name', sa.String(length=1512), nullable=True),
    sa.Column('host_service_name', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_beauty_services_id'), 'beauty_services', ['id'], unique=False)
    op.create_table('plastic_services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service', sa.String(length=512), nullable=True),
    sa.Column('description', sa.String(length=1512), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.Column('old_name', sa.String(length=1512), nullable=True),
    sa.Column('host_service_name', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plastic_services_id'), 'plastic_services', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_plastic_services_id'), table_name='plastic_services')
    op.drop_table('plastic_services')
    op.drop_index(op.f('ix_beauty_services_id'), table_name='beauty_services')
    op.drop_table('beauty_services')
    # ### end Alembic commands ###
