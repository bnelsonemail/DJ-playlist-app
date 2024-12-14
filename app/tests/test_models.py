import pytest
from app import create_app, db
from app.models import Playlist, Song, PlaylistSong, User
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def user(app):
    """Fixture to create a test user."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        yield user




@pytest.mark.usefixtures("app")
class TestModels:
    class TestPlaylist:
        # def test_playlist_model_has_name_and_description(app):
        #     with app.app_context():
        #         # Create a test user
        #         user = User(email="test@example.com", password="hashedpassword")
        #         db.session.add(user)
        #         db.session.commit()

        #         # Create a playlist linked to the user
        #         playlist = Playlist(name="Test Playlist", user_id=user.id)
        #         db.session.add(playlist)
        #         db.session.commit()

        #         assert playlist.name == "Test Playlist"
        #         assert playlist.user_id == user.id


        def test_playlist_has_name_and_user(self, app, user):
            """Ensure Playlist model has name and user_id."""
            with app.app_context():
                playlist = Playlist(name="Test Playlist", user_id=user.id)
                db.session.add(playlist)
                db.session.commit()
                assert playlist.name == "Test Playlist"
                assert playlist.user_id == user.id



        def test_playlist_name_is_required(self, app):
            """Ensure Playlist name is not nullable."""
            with app.app_context():
                with pytest.raises(IntegrityError):
                    playlist = Playlist(name=None)
                    db.session.add(playlist)
                    db.session.commit()



        def test_playlist_description_is_optional(self, app, user):
            """Ensure Playlist description can be None."""
            with app.app_context():

                # create a playlist without a description
                playlist = Playlist(name="My Playlist", user_id=user.id)
                db.session.add(playlist)
                db.session.commit()
                
                # Assert that the description is eth None or an empty string
                assert playlist.description in (None, ""), "Description should be None or an empty string when optional."



        def test_playlist_id_autoincrements(self, app, user):
            """Ensure Playlist ID autoincrements."""
            with app.app_context():
                playlist1 = Playlist(name="Playlist 1", user_id=user.id)
                playlist2 = Playlist(name="Playlist 2", user_id=user.id)
                db.session.add_all([playlist1, playlist2])
                db.session.commit()
                assert playlist1.id < playlist2.id



        # def test_playlist_model_name_is_not_nullable(self, client):
        #     with pytest.raises(Exception):
        #         playlist = Playlist(name=None, description="Test Description")
        #         db.session.add(playlist)
        #         db.session.commit()

        # def test_playlist_model_description_is_nullable(app):
        #     with app.app_context():
        #         user = User(username="testuser", email="test@example.com")
        #         user.set_password("password123")
        #         db.session.add(user)
        #         db.session.commit()

        #         playlist = Playlist(name="My Playlist", user_id=user.id)
        #         db.session.add(playlist)
        #         db.session.commit()

        #         assert playlist.description is None

    class TestSong:
        def test_song_has_title_and_artist(self, app):
            """Ensure Song model has title and artist."""
            with app.app_context():
                song = Song(title="Test Song", artist="Test Artist")
                db.session.add(song)
                db.session.commit()
                assert song.title == "Test Song"
                assert song.artist == "Test Artist"


        def test_song_title_is_required(self, app):
            """Ensure Song title is not nullable."""
            with app.app_context():
                with pytest.raises(IntegrityError):
                    song = Song(title=None, artist="Test Artist")
                    db.session.add(song)
                    db.session.commit()


        # def test_song_model_title_is_not_nullable(self, client):
        #     with pytest.raises(Exception):
        #         song = Song(title=None, artist="Test Artist")
        #         db.session.add(song)
        #         db.session.commit()

        def test_song_id_autoincrements(self, app):
            """Ensure Song ID autoincrements."""
            with app.app_context():
                song1 = Song(title="Song 1", artist="Artist 1")
                song2 = Song(title="Song 2", artist="Artist 2")
                db.session.add_all([song1, song2])
                db.session.commit()
                assert song1.id < song2.id


    class TestPlaylistSong:
        def test_playlist_song_creates_relationship(client, app):
            """Test that PlaylistSong creates relationships correctly."""
            with app.app_context():
                # Create a user first
                user = User(username="testuser", email="test@example.com")
                user.set_password("password123")
                db.session.add(user)
                db.session.commit()

                # Create a playlist and a song
                playlist = Playlist(name="Test Playlist", description="Test Playlist Description", user_id=user.id)
                song = Song(title="Test Song", artist="Test Artist")
                db.session.add_all([playlist, song])
                db.session.commit()

                # Create the relationship
                playlist_song = PlaylistSong(playlist_id=playlist.id, song_id=song.id)
                db.session.add(playlist_song)
                db.session.commit()

                # Validate the relationship
                fetched_playlist_song = PlaylistSong.query.filter_by(
                    playlist_id=playlist.id, song_id=song.id
                ).first()

                assert fetched_playlist_song.playlist_id == playlist.id
                assert fetched_playlist_song.song_id == song.id





        def test_playlist_song_id_autoincrements(self, app, user):
            """Ensure PlaylistSong ID autoincrements."""
            with app.app_context():
                playlist1 = Playlist(name="Playlist 1", user_id=user.id)
                playlist2 = Playlist(name="Playlist 2", user_id=user.id)
                song1 = Song(title="Song 1", artist="Artist 1")
                song2 = Song(title="Song 2", artist="Artist 2")

                db.session.add_all([playlist1, playlist2, song1, song2])
                db.session.commit()

                playlist_song1 = PlaylistSong(playlist_id=playlist1.id, song_id=song1.id)
                playlist_song2 = PlaylistSong(playlist_id=playlist2.id, song_id=song2.id)
                db.session.add_all([playlist_song1, playlist_song2])
                db.session.commit()

                assert playlist_song1.id < playlist_song2.id
            
            
        def test_playlist_creation(self, app):
            with app.app_context():
                user = User(username="testuser", email="test@example.com", password_hash="hashed")
                db.session.add(user)
                db.session.commit()

                playlist = Playlist(name="My Playlist", user_id=user.id)
                db.session.add(playlist)
                db.session.commit()

                assert playlist.id is not None
                assert playlist.user_id == user.id
                assert playlist.name == "My Playlist"


