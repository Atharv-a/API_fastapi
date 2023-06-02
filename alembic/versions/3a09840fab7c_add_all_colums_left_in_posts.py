"""add all colums left in posts

Revision ID: 3a09840fab7c
Revises: f68160dac92c
Create Date: 2023-06-02 18:46:09.607095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a09840fab7c'
down_revision = 'f68160dac92c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,
                                    server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,
                                    server_default=sa.text('now()')))
    
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
