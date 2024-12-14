"""seed.py"""

from app.models import db, Playlist, Song, User, PlaylistSong
from app import create_app

app = create_app()

with app.app_context():
    # Clear existing data to avoid duplicates
    db.session.query(PlaylistSong).delete()  # Clear association table first
    db.session.query(Song).delete()
    db.session.query(Playlist).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create users
    user1 = User(username="musiclover", email="musiclover@example.com")
    user1.set_password("password123")

    # Add user to the session
    db.session.add(user1)

    # Create playlists
    selena_playlist = Playlist(
        name="Selena Gomez Hits",
        description="A playlist of Selena Gomez's popular songs.",
        user=user1
    )

    # Create songs
    song1 = Song(title="Lose You to Love Me", artist="Selena Gomez")
    song2 = Song(title="Rare", artist="Selena Gomez")
    song3 = Song(title="Bad Liar", artist="Selena Gomez")
    song4 = Song(title="Look at Her Now", artist="Selena Gomez")

    # Add songs to the session
    db.session.add_all([song1, song2, song3, song4])

    # Link songs to the playlist via the association table
    selena_playlist.songs.extend([song1, song2, song3, song4])

    # Add the playlist to the session
    db.session.add(selena_playlist)

    # Commit all changes
    db.session.commit()

    print("Users, Selena Gomez songs, and playlists added to the database!")
