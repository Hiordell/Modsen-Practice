"""'initial'

Revision ID: 075cd6b1ab8c
Revises: 
Create Date: 2023-06-21 00:16:23.448370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '075cd6b1ab8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rubrics', sa.String(100), nullable=True),
    sa.Column('text', sa.TEXT(), nullable=False),
    sa.Column('created_data', sa.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('documents')
    # ### end Alembic commands ###