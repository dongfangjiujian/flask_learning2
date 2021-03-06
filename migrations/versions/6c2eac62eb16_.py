"""empty message

Revision ID: 6c2eac62eb16
Revises: 5e77cef8e5a2
Create Date: 2018-09-25 09:50:44.642445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c2eac62eb16'
down_revision = '5e77cef8e5a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.VARCHAR(length=256), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###
