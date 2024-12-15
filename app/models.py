"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    playlists = db.relationship(
        'Playlist',
        back_populates='user',  # Matches the `user` relationship in Playlist
        lazy='dynamic',  # Efficient loading
        cascade="all, delete-orphan",  # Cascades deletes
        passive_deletes=True,  # Delegates deletion handling to the database
    )

    def set_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            raise ValueError("Password hash not set.")
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} (ID: {self.id})>"



# Playlist model
class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True, default="")
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationship with User
    user = db.relationship(
        'User',
        back_populates='playlists',  # Matches the `playlists` relationship in User
    )

    # Relationship with Song through PlaylistSong
    songs = db.relationship(
        'Song',
        secondary='playlist_songs',  # Association table
        back_populates='playlists',  # Matches the `playlists` relationship in Song
        lazy='dynamic',  # Efficient loading for large datasets
    )

    # Direct relationship with PlaylistSong
    playlist_songs = db.relationship(
        'PlaylistSong',
        back_populates='playlist',  # Matches the `playlist` relationship in PlaylistSong
        cascade="all, delete-orphan",  # Cascades deletions
        passive_deletes=True,  # Delegates deletion handling to the database
    )

    def __repr__(self):
        return f"<Playlist {self.name} (ID: {self.id})>"




    # Direct relationship with Playlist
#     playlist = db.relationship(
#         'Playlist',
#         back_populates='playlist_songs',  # Matches the `playlist_songs` relationship in Playlist
#         overlaps="songs",  # Prevents conflicts with the songs relationship
# )





# Song model
class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False, index=True)  # Indexed for efficient queries
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=True)  # Optional album field
    genre = db.Column(db.String(50), nullable=True)  # Optional genre field
    release_year = db.Column(db.Integer, nullable=True)  # Optional release year field
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Many-to-Many relationship with Playlist through PlaylistSong
    playlists = db.relationship(
        'Playlist',
        secondary='playlist_songs',  # Association table
        back_populates='songs',  # Matches the `songs` relationship in Playlist
        overlaps='playlist_songs',  # Prevents conflicts
        lazy='dynamic',  # Efficient loading for large datasets
    )

    # Direct relationship with PlaylistSong
    playlist_songs = db.relationship(
        'PlaylistSong',
        back_populates='song',  # Matches the `song` relationship in PlaylistSong
        overlaps="playlists",  # Prevents conflicts with the playlists relationship
        cascade="all, delete-orphan",  # Cascades deletions
        passive_deletes=True,  # Delegates deletion handling to the database
    )

    def __repr__(self):
        return (
            f"<Song {self.title} by {self.artist} (Genre: {self.genre}, "
            f"Release Year: {self.release_year}, ID: {self.id})>"
        )

    def validate_release_year(self):
        """Validates the release year to ensure it's not in the future."""
        current_year = datetime.utcnow().year
        if self.release_year and self.release_year > current_year:
            raise ValueError("Release year cannot be in the future.")

    def add_to_playlist(self, playlist):
        """Adds the song to a playlist if not already added."""
        if not isinstance(playlist, Playlist):
            raise ValueError("Invalid playlist object.")
        if playlist not in self.playlists:
            self.playlists.append(playlist)



# PlaylistSong model
class PlaylistSong(db.Model):
    __tablename__ = 'playlist_songs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(
        db.Integer, 
        db.ForeignKey('playlists.id', ondelete='CASCADE'), 
        nullable=False, 
        index=True
    )
    song_id = db.Column(
        db.Integer, 
        db.ForeignKey('songs.id', ondelete='CASCADE'), 
        nullable=False, 
        index=True
    )
    created_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow,
        server_default=db.func.now()
    )

    playlist = db.relationship(
        'Playlist',
        back_populates='playlist_songs',  # Matches the `playlist_songs` relationship in Playlist
        overlaps="songs",
    )

    song = db.relationship(
        'Song',
        back_populates='playlist_songs',  # Matches the `playlist_songs` relationship in Song
        overlaps="playlists",
    )

    __table_args__ = (
        db.UniqueConstraint('playlist_id', 'song_id', name='unique_playlist_song'),
    )

    def __repr__(self):
        return (
            f"<PlaylistSong (ID: {self.id}, "
            f"Playlist: {self.playlist.name if self.playlist else 'N/A'}, "
            f"Song: {self.song.title if self.song else 'N/A'}, "
            f"Created At: {self.created_at})>"
        )


    @staticmethod
    def create_relationship(playlist, song):
        """Creates a PlaylistSong relationship with validation."""
        if not isinstance(playlist, Playlist):
            raise ValueError("Invalid playlist object.")
        if not isinstance(song, Song):
            raise ValueError("Invalid song object.")
        return PlaylistSong(playlist=playlist, song=song)





# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
