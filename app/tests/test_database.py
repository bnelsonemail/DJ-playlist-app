import pytest
from app import db
from app.models import Playlist, Song, User  # Adjust import paths as necessary


def test_database_setup_function(test_database_setup):
    """Test that the database setup fixture works as expected."""

    # Step 1: Verify initial data setup
    playlist = Playlist.query.first()
    song = Song.query.first()

    assert playlist is not None, "Playlist should be created by the fixture."
    assert song is not None, "Song should be created by the fixture."
    assert "Initial Playlist" in playlist.name, "Playlist name should match the initial setup."
    assert "Initial Song" in song.title, "Song title should match the initial setup."

    # Step 2: Add temporary data to test rollback behavior
    user = User.query.first()  # Fetch the existing user set up by the fixture
    assert user is not None, "User should be created by the fixture."

    temp_playlist = Playlist(name="Temporary Playlist", description="Temporary Description", user_id=user.id)
    temp_song = Song(title="Temporary Song", artist="Temporary Artist")

    db.session.add(temp_playlist)
    db.session.add(temp_song)
    db.session.commit()

    # Verify the temporary data was added
    assert Playlist.query.filter_by(name="Temporary Playlist").first() is not None
    assert Song.query.filter_by(title="Temporary Song").first() is not None

    # Step 3: Verify that rollback occurs after test (done implicitly by the fixture)

# Step 4: Test that temporary data is cleaned up
@pytest.fixture(autouse=True)
def check_cleanup():
    yield
    # Run after each test
    temp_playlist = Playlist.query.filter_by(name="Temporary Playlist").first()
    temp_song = Song.query.filter_by(title="Temporary Song").first()

    assert temp_playlist is None, "Temporary playlist should not persist after test."
    assert temp_song is None, "Temporary song should not persist after test."
