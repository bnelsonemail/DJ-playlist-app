"""Fix relationship backref

Revision ID: deabb5c02b6c
Revises: 95946548f1c4
Create Date: 2024-12-11 02:27:44.346178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deabb5c02b6c'
down_revision = '95946548f1c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('songs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('artist', sa.String(length=100), nullable=False),
    sa.Column('album', sa.String(length=100), nullable=True),
    sa.Column('genre', sa.String(length=50), nullable=True),
    sa.Column('release_year', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_songs_title'), ['title'], unique=False)

    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    op.create_table('playlists',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('playlists', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_playlists_user_id'), ['user_id'], unique=False)

    op.create_table('playlist_songs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('playlist_id', sa.Integer(), nullable=False),
    sa.Column('song_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlists.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['song_id'], ['songs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('playlist_id', 'song_id', name='unique_playlist_song')
    )
    with op.batch_alter_table('playlist_songs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_playlist_songs_playlist_id'), ['playlist_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_playlist_songs_song_id'), ['song_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('playlist_songs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_playlist_songs_song_id'))
        batch_op.drop_index(batch_op.f('ix_playlist_songs_playlist_id'))

    op.drop_table('playlist_songs')
    with op.batch_alter_table('playlists', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_playlists_user_id'))

    op.drop_table('playlists')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_songs_title'))

    op.drop_table('songs')
    # ### end Alembic commands ###
