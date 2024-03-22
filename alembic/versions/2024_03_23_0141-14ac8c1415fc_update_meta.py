"""update meta

Revision ID: 14ac8c1415fc
Revises: 
Create Date: 2024-03-23 01:41:11.256680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '14ac8c1415fc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('albumTags_1')
    op.drop_table('albumFiles_1')
    op.drop_table('albumFiles_2')
    op.drop_table('albumTags_2')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albumTags_2',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('file_album_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True, comment='Не конкретно файл айди, а айди записи внутри альбома для этого файла'),
    sa.Column('tag', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('added_at', mysql.DATETIME(), nullable=True),
    sa.Column('added_by', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['added_by'], ['user.id'], name='albumTags_2_ibfk_2', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['file_album_id'], ['albumFiles_2.id'], name='albumTags_2_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('albumFiles_2',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('file_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('name', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('type', mysql.VARCHAR(length=16), nullable=True),
    sa.Column('pinned_at', mysql.DATETIME(), nullable=True),
    sa.Column('pinned_by', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['pinned_by'], ['user.id'], name='albumFiles_2_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('albumFiles_1',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('file_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('name', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('type', mysql.VARCHAR(length=16), nullable=True),
    sa.Column('pinned_at', mysql.DATETIME(), nullable=True),
    sa.Column('pinned_by', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['pinned_by'], ['user.id'], name='albumFiles_1_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('albumTags_1',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('file_album_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True, comment='Не конкретно файл айди, а айди записи внутри альбома для этого файла'),
    sa.Column('tag', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('added_at', mysql.DATETIME(), nullable=True),
    sa.Column('added_by', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['added_by'], ['user.id'], name='albumTags_1_ibfk_2', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['file_album_id'], ['albumFiles_1.id'], name='albumTags_1_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###