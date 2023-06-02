"""Create Post table

Revision ID: 1112799aa961
Revises: 
Create Date: 2023-06-02 18:01:19.460864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1112799aa961'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass


