"""update meta

Revision ID: 8f244da3d9f8
Revises: 
Create Date: 2024-03-23 00:49:14.842187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f244da3d9f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=128, collation='utf8mb4_general_ci'), nullable=True),
    sa.Column('username', sa.String(length=63), nullable=True),
    sa.Column('avatar_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=63), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('base_album', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4'
    )
    op.create_table('albumsAccess',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('editor', sa.BOOLEAN(), nullable=True),
    sa.Column('viewer', sa.BOOLEAN(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('accessed_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['accessed_by'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('albumsMeta',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('private', sa.BOOLEAN(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128, collation='utf8mb4_general_ci'), nullable=True),
    sa.Column('description', sa.String(length=512, collation='utf8mb4_general_ci'), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('albumsMeta')
    op.drop_table('albumsAccess')
    op.drop_table('user')
    # ### end Alembic commands ###
