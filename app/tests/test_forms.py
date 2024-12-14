from flask_wtf.csrf import generate_csrf
from wtforms.validators import ValidationError
from app import app, create_app, db
from app.forms import SongForm, PlaylistForm
from app.models import Song
import pytest

@pytest.fixture
def app():
    """Set up Flask application for testing forms."""
    app = create_app("testing")
    with app.app_context():
        yield app
        
        
# @pytest.fixture
# def test_app():
#     """Provide a Flask test app context."""
#     with app.test_request_context():
#         yield

@pytest.mark.usefixtures("app")
class TestSongForm:
    def test_song_form_has_title_and_artist_fields(self, app):
        """Test that SongForm contains title and artist fields."""
        with app.test_request_context():
            form = SongForm()
            assert "title" in form._fields
            assert "artist" in form._fields




    def test_song_form_doesnt_include_unexpected_fields(self, app):
        """Test that SongForm doesn't contain unexpected fields."""
        expected_fields = {"title", "artist", "genre", "release_year", "album"} 
        with app.app_context():
            form = SongForm()
            form.title.data = 'sample-title'
            form.artist.data = 'sample-artist'
            
            # Validate actual fields against expected fields
            actual_fields = set(form._fields.keys())
            unexpected_fields = actual_fields - expected_fields
            
            # Log for debugging
            print(f"Actual fields: {actual_fields}")
            print(f"Expected fields: {expected_fields}")
            
            # Ensure no unexpected fields are present
            assert not unexpected_fields, f"Unexpected fields found: {unexpected_fields}"


    def test_song_form_validation_is_working(self, app):
        app = create_app('testing')  # Create the app in test mode
        with app.app_context():      # Use app context
            form = SongForm(data={"title": "Test", "artist": "Test Artist"})
            assert form.validate() is True


    def test_song_form_validate_title(self, app, test_database_setup):
        """Test that SongForm's validate_title checks for duplicate titles."""
        with app.app_context():
            # Add a song to the database
            song = Song(title="Test Title", artist="Test Artist")
            db.session.add(song)
            db.session.commit()

            # Debug log for verification
            print("Added song to database:", song)

            # Verify that the song was added to the database
            retrieved_song = Song.query.filter_by(title="Test Title").first()
            assert retrieved_song is not None, "The song should exist in the database."
            assert retrieved_song.title == "Test Title", "The song title should match the one added."

            # Create a form with the same title to simulate duplicate entry
            form = SongForm(data={"title": "Test Title", "artist": "Another Artist"})

            # Validate the title using the form's custom validation
            with pytest.raises(ValidationError, match="This song title already exists.") as exc_info:
                form.validate_title(form.title)

            # Debug log for validation error
            print("Validation error raised as expected:", exc_info.value)

            # Ensure the form fails validation due to the duplicate title
            assert not form.validate(), "Form validation should fail due to a duplicate title."
            assert "This song title already exists." in form.errors["title"], (
                "The form should contain the appropriate validation error for the duplicate title."
            )





@pytest.mark.usefixtures("app")
class TestPlaylistForm:
    def test_playlist_form_includes_name_and_description_fields(self, app):
        """Test that PlaylistForm contains 'name' and 'description' fields."""
        with app.app_context():
            form = PlaylistForm()
            assert "name" in form.data
            assert "description" in form.data


    def test_playlist_form_doesnt_include_unexpected_fields(self, app):
        """Test that PlaylistForm doesn't contain unexpected fields."""
        expected_fields = {"name", "description"}
        with app.app_context(): 
            form = PlaylistForm()
            # form.name.data = 'sample-name'
            # form.description.data = 'sample-description'

            # Validate actual fields against expected fields
            actual_fields = set(form._fields.keys())
            unexpected_fields = actual_fields - expected_fields
            
            # Log for debugging
            print(f"Actual fields: {actual_fields}")
            print(f"Expected fields: {expected_fields}")
            
            # Ensure no unexpected fields are present
            assert not unexpected_fields, f"Unexpected fields found: {unexpected_fields}"


    def test_playlist_form_validation_is_working(self, app):
        """Test PlaylistForm validation logic."""
        with app.app_context(): 
            # Test invalid form (empty fields)
            form = PlaylistForm(name='', description='')
            assert not form.validate()

            # Test valid form (filled fields)
            form = PlaylistForm(name='Test Playlist', description='Test Description')
            assert form.validate()


