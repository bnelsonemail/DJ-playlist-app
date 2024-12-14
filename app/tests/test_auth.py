"""Tests for authentication in the Playlists Manager application."""

import pytest
# import pdb; pdb.set_trace()
from app.models import User, db



# @pytest.fixture
# def test_client(app):
#     """Fixture to create a test client."""
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#             yield client
#             db.session.remove()
#             db.drop_all()


# @pytest.fixture
# def csrf_token(client):
#     """Fetch a CSRF token from a route with a form."""
#     response = client.get("/auth/login")  # Replace with a form route
#     assert response.status_code == 200
#     token = response.data.decode("utf-8").split('name="csrf_token" value="')[1].split('"')[0]
#     return token



# @pytest.fixture
# def user():
#     """Fixture to create a test user."""
#     with app.app_context():
#         # Create a user
#         user = User(username="testuser", email="test@example.com")
#         user.set_password("password123")  # Use set_password to hash the password
#         db.session.add(user)
#         db.session.commit()



def test_register(client, app):
    with app.app_context():
        print("Accessing registration endpoint...")
        response = client.post(
            "/auth/register",
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=True,
        )
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data.decode('utf-8')}")
        assert response.status_code == 200
        assert b"Account created successfully" in response.data  # Match flash message
        assert User.query.filter_by(email="test@example.com").first() is not None




@pytest.fixture
def setup_user(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")  # Use the set_password method
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.rollback()



def test_login_valid_credentials(client, setup_user):
    """Test login with valid credentials."""
    
    # Log in with valid credentials
    response = client.post(
        "/auth/login",
        data={"email": "test@example.com", "password": "password123"},
        follow_redirects=True
    )
    
    # Check response status and flash message
    assert response.status_code == 200
    assert b"Logged in successfully!" in response.data




def test_login_invalid_credentials(client, setup_user):
    """Test login with invalid credentials."""
    # Attempt login with incorrect email and password

    response = client.post(
        "/auth/login",
        data={
            "email": "wrong@example.com",
            "password": "wrongpassword",
        },
        follow_redirects=True,  
    )
    assert response.status_code == 200
    assert b"Invalid email or password." in response.data




def test_logout(client, setup_user):
    """Test user logout."""
    # Log in the user
    login_response = client.post(
        "/auth/login",
        data={"email": setup_user.email, "password": "password123"},
        follow_redirects=True,
    )
    assert login_response.status_code == 200
    assert b"Logged in successfully!" in login_response.data

    # Log out the user
    logout_response = client.get("/auth/logout", follow_redirects=True)
    assert logout_response.status_code == 200
    assert b"You have been logged out." in logout_response.data




