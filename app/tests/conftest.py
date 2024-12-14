"""app/tests/conftest.py"""

import pytest
import logging
import uuid
from app import create_app, db
from app.models import User, Playlist, Song  # Import all required models
from sqlalchemy.sql import text


@pytest.fixture
def app():
    """Set up Flask application for testing."""
    app = create_app('testing')  # Use testing config
    with app.app_context():
        db.create_all()  # Create tables for tests
        print("Created all tables for testing")  # Debug log
        try:
            yield app  # Test runs here
        finally:
            print("Rolling back and cleaning up the database")  # Debug log
            db.session.rollback()  # Rollback any uncommitted transactions
            db.session.remove()  # Remove the session
            db.session.close()  # Close the session explicitly
            db.drop_all()  # Drop all tables
            print("Dropped all tables")  # Debug log


@pytest.fixture
def test_client(app):
    """A test client using the app fixture."""
    return app.test_client()


@pytest.fixture
def test_user(app, test_database_setup):
    """Create and provide a test user."""
    with app.app_context():
        unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
        unique_email = f"{unique_username}@example.com"
        user = User(username=unique_username, email=unique_email)
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()


@pytest.fixture
def client(app):
    """Test client fixture using the app context."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def runner(app):
    """Set up CLI runner."""
    return app.test_cli_runner()




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def test_database_setup(app):
    """Set up the test database with schema-based isolation."""
    logger.info("Starting test database setup.")

    with app.app_context():
        test_schema = f"test_schema_{uuid.uuid4().hex[:8]}"
        logger.info(f"Creating test schema: {test_schema}")

        with db.engine.connect() as connection:
            try:
                # Create and switch to the test schema
                connection.execute(text(f"CREATE SCHEMA {test_schema};"))
                connection.execute(text(f"SET search_path TO {test_schema};"))

                # Create tables within the test schema
                db.create_all()
                logger.info("Tables created in the test schema.")

                # Add initial test data
                user = User(
                    username=f"testuser_{uuid.uuid4()}",
                    email=f"testuser_{uuid.uuid4()}@example.com"
                )
                user.set_password("password123")
                playlist = Playlist(
                    name=f"Initial Playlist {uuid.uuid4()}",
                    description="Initial Description",
                    user_id=user.id
                )
                song = Song(
                    title=f"Initial Song {uuid.uuid4()}",
                    artist="Initial Artist"
                )

                db.session.add_all([user, playlist, song])
                db.session.commit()
                logger.info("Initial test data added.")

                # Validate setup
                assert User.query.count() == 1, "User setup failed."
                assert Playlist.query.count() == 1, "Playlist setup failed."
                assert Song.query.count() == 1, "Song setup failed."

                yield db  # Provide the test database session to the test

            finally:
                logger.info("Rolling back and cleaning up.")
                db.session.rollback()
                db.session.remove()

                # Drop the test schema
                try:
                    connection.execute(text(f"DROP SCHEMA {test_schema} CASCADE;"))
                    logger.info(f"Test schema {test_schema} dropped.")
                except Exception as e:
                    logger.error(f"Error dropping test schema: {e}")





