"""adding more columns to post

Revision ID: 496595b20693
Revises: 1112799aa961
Create Date: 2023-06-02 18:19:29.166455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '496595b20693'
down_revision = '1112799aa961'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
