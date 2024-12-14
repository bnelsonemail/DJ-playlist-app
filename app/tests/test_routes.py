"""Tests for routes.py in the Playlists Manager application."""

import pytest
import html
import logging
import uuid
from flask import url_for
from app import create_app, db
from app.models import Playlist, Song, User

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.fixture
def app():
    """Set up Flask app for testing."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        # Seed the database with a test user
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Set up test client."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_playlists(app, test_user):
    """Create test playlists for the user."""
    def _create_playlists(name="Test Playlist", description="A sample playlist"):
        with app.app_context():
            playlist = Playlist(name=name, description=description, user_id=test_user.id)
            db.session.add(playlist)
            db.session.commit()
            return playlist

    return _create_playlists




@pytest.fixture
def logged_in_client(client, app):
    """Fixture to log in a dynamically created test user."""
    user = None  # Initialize user to avoid reference errors in the cleanup phase.
    
    with app.app_context():
        try:
            # Generate unique user details for the test
            unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
            unique_email = f"{unique_username}@example.com"
            logger.info(f"Creating test user: {unique_username}, {unique_email}")

            # Create the test user
            user = User(username=unique_username, email=unique_email)
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()
            logger.info("Test user created successfully.")

            # Log in the test user via the Flask client
            response = client.post(
                "/auth/login",
                data={"email": unique_email, "password": "password123"},
                follow_redirects=True,
            )
            assert response.status_code == 200, "Login failed during fixture setup."
            assert b"Welcome" in response.data or b"Dashboard" in response.data, "Unexpected login response."
            logger.info("Test user logged in successfully.")

            yield client  # Provide the logged-in client to the test

        except Exception as e:
            logger.error(f"Error during logged_in_client setup: {e}")
            raise

        finally:
            # Cleanup: Remove the test user and rollback the session
            try:
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    logger.info("Test user cleaned up successfully.")
            except Exception as cleanup_error:
                logger.error(f"Error during test user cleanup: {cleanup_error}")
            finally:
                db.session.remove()
                logger.info("Database session removed.")








class TestRoutes:
    """Tests for the route functionality."""
    
    
    def test_homepage_redirects_to_playlists(logged_in_client, setup_playlists):
        """Test that the homepage redirects to playlists for logged-in users."""
        response = logged_in_client.get("/", follow_redirects=True)
        assert response.status_code == 200
        assert b"See all the playlists!" in response.data




    def test_playlists_page_logged_out(self, client):
        """Test that /playlists requires login."""
        response = client.get("/playlists", follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page." in response.data



    def test_playlists_page_logged_in(logged_in_client, setup_playlists):
        """Test that /playlists is accessible for logged-in users."""
        with logged_in_client.application.app_context():
            # Create test playlists
            playlist1 = setup_playlists(name="Playlist 1", description="Description 1")
            playlist2 = setup_playlists(name="Playlist 2", description="Description 2")

        response = logged_in_client.get("/playlists", follow_redirects=True)

        # Assert response status and content
        assert response.status_code == 200, "Expected HTTP 200 status code for the playlists page."
        assert b"Your Playlists" in response.data, "Page should display the playlists heading."
        assert b"Playlist 1" in response.data, "Page should list 'Playlist 1'."
        assert b"Playlist 2" in response.data, "Page should list 'Playlist 2'."







    def test_add_playlist(logged_in_client, app, test_user):
        """Test adding a playlist."""
        # Send a POST request to add a playlist
        response = logged_in_client.post(
            "/playlists/add",
            data={"name": "My Playlist", "description": "This is a test playlist"},
            follow_redirects=True,
        )

        # Assert the response
        assert response.status_code == 200, "Expected HTTP 200 status code for successful POST."
        assert b"My Playlist" in response.data, "Playlist name not found in response."

        # Verify the playlist was added to the database
        with app.app_context():
            playlist = Playlist.query.filter_by(name="My Playlist").first()
            assert playlist is not None, "Playlist was not added to the database."
            assert playlist.description == "This is a test playlist", "Playlist description is incorrect."
            assert playlist.user_id == test_user.id, "Playlist ownership is incorrect."




    def test_add_song(self, client, test_user):
        """Test adding a new song."""
        # Log in the test user
        client.post(
            "/auth/login",
            data={"email": test_user.email, "password": "password123"},
            follow_redirects=True,
        )

        # Add the song
        response = client.post(
            "/songs/add",
            data={
                "title": "Test Song",
                "artist": "Test Artist",
            },
            follow_redirects=True,
        )

        # Check if the song was added successfully
        assert response.status_code == 200
        assert b"Song added successfully!" in response.data
        assert b"Test Song" in response.data
        assert b"Test Artist" in response.data


    @pytest.mark.usefixtures("test_database_setup")
    def test_add_song_to_playlist(logged_in_client, test_user, setup_playlists):
        """Test adding a song to a playlist."""
        logger.info("Starting test_add_song_to_playlist")

        with logged_in_client.application.app_context():
            # Retrieve or create the test playlist using setup_playlists fixture
            playlist = setup_playlists(name="Test Playlist", description="Sample Test Playlist")
            assert playlist is not None, "Test playlist should exist."
            logger.info(f"Test playlist created: {playlist.name} (ID: {playlist.id})")

            # Simulate adding songs to the database
            logger.info("Adding songs to the database.")
            song1 = Song(title="Song One", artist="Artist One")
            song2 = Song(title="Song Two", artist="Artist Two")
            db.session.add_all([song1, song2])
            db.session.commit()

            # Validate that the songs are in the database
            added_songs = Song.query.filter(Song.title.in_(["Song One", "Song Two"])).all()
            assert len(added_songs) == 2, "Both songs should exist in the database."
            logger.info(f"Songs added to database: {[song.title for song in added_songs]}")

            # Add song2 to the playlist via POST request
            logger.info("Adding song2 to playlist via POST request.")
            response = logged_in_client.post(
                url_for("main.add_song_to_playlist", playlist_id=playlist.id),
                data={"song": song2.id},
                follow_redirects=True,
            )

            # Verify response status and success message
            logger.info("Verifying response and success message.")
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."
            response_text = response.get_data(as_text=True)
            success_message = f"Added '{song2.title}' to playlist '{playlist.name}'."
            assert success_message in response_text, f"Expected success message '{success_message}' not found in response."

            # Validate that song2 is associated with the playlist
            updated_playlist = Playlist.query.get(playlist.id)
            assert updated_playlist is not None, "Updated playlist should exist."
            assert song2 in updated_playlist.songs, f"'{song2.title}' should be in the playlist '{playlist.name}'."
            logger.info(f"Verified that '{song2.title}' is associated with playlist '{playlist.name}'.")

            # Ensure song1 is still available for selection
            available_songs = Song.query.filter(~Song.id.in_({song.id for song in updated_playlist.songs})).all()
            assert song1 in available_songs, f"'{song1.title}' should still be available for selection."
            logger.info(f"'{song1.title}' is still available for selection.")







    def test_delete_song(self, logged_in_client):
        """Test deleting a song."""
        # Create a song
        with logged_in_client.application.app_context():
            song = Song(title="Delete Me", artist="Delete Artist")
            db.session.add(song)
            db.session.commit()

        response = logged_in_client.post(
            url_for("main.delete_song", song_id=1),
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"has been deleted." in response.data



    def test_edit_playlist(logged_in_client, setup_playlists):
        """Test editing a playlist."""
        with logged_in_client.application.app_context():
            # Get the logged-in user
            with logged_in_client.session_transaction() as session:
                user_id = session["_user_id"]

            # Create a playlist for the logged-in user
            playlist = setup_playlists(name="Old Playlist", description="Old Description")
            assert playlist.user_id == int(user_id), "Playlist should belong to the logged-in user."

        # Edit the playlist
        response = logged_in_client.post(
            url_for("main.edit_playlist", playlist_id=playlist.id),
            data={"name": "Updated Playlist", "description": "Updated Description"},
            follow_redirects=True,
        )

        # Assertions for response and database changes
        assert response.status_code == 200, "Expected HTTP 200 status code for a successful edit."
        assert b"Playlist 'Updated Playlist' has been updated." in response.data

        with logged_in_client.application.app_context():
            updated_playlist = Playlist.query.get(playlist.id)
            assert updated_playlist.name == "Updated Playlist", "Playlist name was not updated."
            assert updated_playlist.description == "Updated Description", "Playlist description was not updated."




