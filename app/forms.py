""" playlist_app/forms.py """

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
)
from app.models import User, Song, db


class PlaylistForm(FlaskForm):
    """Form for creating or editing playlists."""
    name = StringField("Playlist Name", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=200)])


class SongForm(FlaskForm):
    """Form for creating or editing a song."""
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=200)],
    )
    artist = StringField(
        "Artist",
        validators=[DataRequired(), Length(max=200)],
    )
    album = StringField(
        "Album",
        validators=[Optional(), Length(max=200)],
    )
    genre = SelectField(
        "Genre",
        choices=[
            ("rock", "Rock"),
            ("pop", "Pop"),
            ("hip_hop", "Hip Hop"),
            ("jazz", "Jazz"),
            ("classical", "Classical"),
            ("other", "Other"),
        ],
        validators=[Optional()],
        default="other",  # Default genre
    )
    release_year = IntegerField(
        "Release Year",
        validators=[Optional(), NumberRange(min=1900, max=2100)],
    )

    def validate_title(self, title):
        """Custom validation for unique song title."""
        # Ensure a database session is bound
        if db.session.bind:
            song_query = Song.query.filter_by(title=title.data)
            # Ensure the query excludes the current song if editing
            if hasattr(self, 'song_id') and self.song_id:
                song_query = song_query.filter(Song.id != self.song_id)

            # Check if a song with the same title exists
            if song_query.first():
                raise ValidationError("This song title already exists. Please choose a different title.")

    def set_song_id(self, song_id):
        """Set the current song ID for edit validation."""
        self.song_id = song_id




class NewSongForPlaylistForm(FlaskForm):
    """Form for adding an existing song to a playlist."""
    song = SelectField(
        "Song To Add", 
        coerce=int, 
        validators=[DataRequired(message="You must select a song to add.")],
    )
    submit = SubmitField("Add Song")


class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match.")
    ])
    submit = SubmitField("Register")


    def validate_email(self, email):
        """Check for duplicate email."""
        try:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email is already registered.")
        except Exception as e:
            raise ValidationError(f"Database error during email validation: {e}")


    def validate_username(self, username):
        """Check for duplicate username."""
        try:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is already taken.")
        except Exception as e:
            raise ValidationError(f"Database error during username validation: {e}")



class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
