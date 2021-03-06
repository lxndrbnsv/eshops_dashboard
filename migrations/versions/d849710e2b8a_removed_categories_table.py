"""removed Categories table

Revision ID: d849710e2b8a
Revises: 042b4a2d50c2
Create Date: 2021-02-01 11:11:32.016356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd849710e2b8a'
down_revision = '042b4a2d50c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scraper_category', sa.Column('cat_name', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scraper_category', 'cat_name')
    # ### end Alembic commands ###
