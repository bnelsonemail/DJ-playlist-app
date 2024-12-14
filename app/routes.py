"""app/routes.py"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, sessions, current_app
from app.models import Playlist, Song, db
from app.forms import NewSongForPlaylistForm, SongForm, PlaylistForm, LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
import logging

# Create a blueprint
main_bp = Blueprint('main', __name__)

# LOGIN PAGE
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('main.show_all_playlists'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)


# SHOW ALL PLAYLISTS
@main_bp.route('/playlists')
@login_required
def show_all_playlists():
    """Show all playlists for the logged-in user."""
    playlists = Playlist.query.filter_by(user_id=current_user.id).all()
    songs = Song.query.all()  # Fetch songs if needed
    form = SongForm()  # Use the appropriate form here, e.g., SongForm

    # Log the playlists and their songs for debugging
    for playlist in playlists:
        print(f"Playlist: {playlist.name}, Songs: {playlist.songs}")

    return render_template('playlists.html', playlists=playlists, songs=songs, form=form)



@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    current_app.logger.debug(f"Request: {request.method} {request.url}")
    
    # Create the form with incoming request data
    form = RegistrationForm(request.form)

    # Log incoming form data for debugging
    current_app.logger.debug(f"Form data: {request.form}")

    if request.method == 'POST':
        current_app.logger.debug("Processing POST request")
        
        # Validate the form
        if form.validate_on_submit():
            try:
                # Create and save the new user
                user = User(
                    username=form.username.data,
                    email=form.email.data,
                )
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                
                # Log the user in after registration
                login_user(user)
                flash('Registration successful! Welcome!', 'success')
                current_app.logger.debug("Registration successful")

                # Redirect to main page
                return redirect(url_for('main.show_all_playlists'))
            except Exception as e:
                # Handle database errors
                db.session.rollback()
                current_app.logger.error(f"Database error: {e}")
                flash('An error occurred during registration. Please try again.', 'danger')
        else:
            # Log form errors
            current_app.logger.debug(f"Form validation failed: {form.errors}")
            flash('There were errors in your form. Please correct them.', 'danger')

    return render_template('register.html', form=form)




@main_bp.route("/")
def root():
    """Homepage: redirect to /playlists."""
    return redirect("/playlists")


# SHOW SINGLE PLAYLIST
@main_bp.route("/playlists/<int:playlist_id>")
@login_required
def show_playlist(playlist_id):
    """Show a single playlist for the user."""
    # Fetch the playlist by ID and ensure it belongs to the current user
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        flash("You do not have permission to view this playlist.", "danger")
        return redirect(url_for('main.show_all_playlists'))

    # Log playlist details for debugging
    print(f"Playlist '{playlist.name}' contains songs: {playlist.songs.all()}")

    # Render the template for a single playlist
    return render_template('show_playlist.html', playlist=playlist, form=SongForm())



# ADD PLAYLIST
@main_bp.route("/playlists/add", methods=["GET", "POST"])
@login_required
def add_playlist():
    """Handle add-playlist form."""
    form = PlaylistForm()

    if form.validate_on_submit():
        # Extract form data
        name = form.name.data
        description = form.description.data

        # Create a new Playlist instance with the current user's ID
        playlist = Playlist(name=name, description=description, user_id=current_user.id)
        db.session.add(playlist)
        db.session.commit()

        # Flash success message
        flash("Playlist created successfully!", "success")

        # Redirect back to the playlists page
        return redirect(url_for("main.show_all_playlists"))

    # Render the new_playlist.html template with the form
    return render_template("new_playlist.html", form=form)


# SHOW ALL SONGS ON SONG.HTML PAGE
@main_bp.route('/songs')
@login_required
def show_all_songs():
    """Show all songs for the user."""
    songs = Song.query.all()  # Fetch all songs
    playlists = Playlist.query.filter_by(user_id=current_user.id).all()
    form = SongForm()  # Instantiate the form if needed for hidden_tag
    return render_template("songs.html", songs=songs, playlists=playlists, form=form)





# ADD SONGS
@main_bp.route("/songs/add", methods=["GET", "POST"])
@login_required
def add_song():
    """Handle add-song form."""
    form = SongForm()

    if form.validate_on_submit():
        new_song = Song(
            title=form.title.data,
            artist=form.artist.data,
            album=form.album.data if hasattr(Song, 'album') else None,
            genre=form.genre.data if hasattr(Song, 'genre') else None,
            release_year=form.release_year.data if hasattr(Song, 'release_year') else None,
        )
        db.session.add(new_song)
        db.session.commit()
        flash("Song added successfully!", "success")
        return redirect(url_for("main.show_all_songs"))

    return render_template("new_song.html", form=form)




# ADD SONGS TO PLAYLIST FROM USER PAGE
@main_bp.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
@login_required
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist."""
    # Fetch the playlist or return a 404 error if not found
    playlist = Playlist.query.get_or_404(playlist_id)

    # Ensure the playlist belongs to the logged-in user
    if playlist.user_id != current_user.id:
        flash("You do not have permission to modify this playlist.", "danger")
        return redirect(url_for("main.show_all_playlists"))

    # Initialize the form for adding a song to the playlist
    form = NewSongForPlaylistForm()

    # Get the list of songs not already in the playlist using an explicit subquery
    subquery = db.session.query(PlaylistSong.song_id).filter_by(playlist_id=playlist.id).subquery()
    available_songs = Song.query.filter(Song.id.notin_(subquery)).all()

    # Populate the dropdown with the available songs
    form.song.choices = [(song.id, f"{song.title} by {song.artist}") for song in available_songs]

    if form.validate_on_submit():
        try:
            # Fetch the selected song
            song_id = form.song.data
            song = Song.query.get_or_404(song_id)

            # Add the song to the playlist
            playlist.songs.append(song)
            db.session.commit()

            # Flash success message
            flash(f"Added '{song.title}' to playlist '{playlist.name}'.", "success")
            return redirect(url_for("main.show_playlist", playlist_id=playlist.id))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while adding the song to the playlist. Please try again.", "danger")
            current_app.logger.error(f"Error adding song {song_id} to playlist {playlist_id}: {e}")

    return render_template("add_song_to_playlist.html", form=form, playlist=playlist)



# ADD SONG FROM SONGS.HTML PAGE
@main_bp.route("/songs/add-to-playlist", methods=["POST"])
@login_required
def add_song_to_playlist_from_songs():
    """Handle adding a song to a playlist from the songs list."""
    # Retrieve form data
    logging.info(f"Form data received: {request.form}")
    song_id = request.form.get("song_id")
    playlist_id = request.form.get("playlist_id")
    logging.info(f"Song ID: {song_id}, Playlist ID: {playlist_id}")

    # Validate IDs
    song = Song.query.get(song_id)
    playlist = Playlist.query.get(playlist_id)


    if not song or not playlist:
        flash("Invalid song or playlist selected.", "danger")
        return redirect(url_for("main.show_all_songs"))

    # Ensure the playlist belongs to the logged-in user
    if playlist.user_id != current_user.id:
        flash("You are not authorized to modify this playlist.", "danger")
        return redirect(url_for("main.show_all_songs"))

    # Add the song to the playlist
    playlist.songs.append(song)
    db.session.commit()
    flash(f"'{song.title}' has been added to '{playlist.name}'.", "success")
    
    
    # Fetch the song and playlist
    # song = Song.query.get_or_404(song_id)
    # playlist = Playlist.query.get_or_404(playlist_id)

    # Add the song to the playlist
    # if song not in playlist.songs:
    #     playlist.songs.append(song)
    #     db.session.commit()
    #     flash(f"Added '{song.title}' to playlist '{playlist.name}'.", "success")
    # else:
    #     flash(f"'{song.title}' is already in playlist '{playlist.name}'.", "info")

    # Redirect back to the songs page
    return redirect(url_for("main.show_all_songs"))


# DELETE SONG ROUTE
@main_bp.route("/songs/<int:song_id>/delete", methods=["POST"])
@login_required
def delete_song(song_id):
    """Delete a song."""
    song = Song.query.get_or_404(song_id)

    # # Check if the song is in any playlists
    # if song.playlists.count() > 0:
    #     flash("Cannot delete a song that is part of a playlist.", "danger")
    #     return redirect(url_for("main.show_all_songs"))

    # Delete the song
    db.session.delete(song)
    db.session.commit()
    flash(f"'{song.title}' by {song.artist} has been deleted.", "success")
    return redirect(url_for("main.show_all_songs"))


# DELETE A PLAYLIST
@main_bp.route("/playlists/<int:playlist_id>/delete", methods=["POST"])
@login_required
def delete_playlist(playlist_id):
    """Delete a playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)

    # Ensure the playlist belongs to the logged-in user
    if playlist.user_id != current_user.id:
        flash("You are not authorized to delete this playlist.", "danger")
        return redirect(url_for("main.show_all_playlists"))

    # Delete the playlist
    db.session.delete(playlist)
    db.session.commit()
    flash(f"Playlist '{playlist.name}' has been deleted.", "success")
    return redirect(url_for("main.show_all_playlists"))


# EDIT A PLAYLIST
@main_bp.route('/playlists/<int:playlist_id>/edit', methods=["GET", "POST"])
@login_required
def edit_playlist(playlist_id):
    """Edit a playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)

    # Ensure the playlist belongs to the logged-in user
    if playlist.user_id != current_user.id:
        flash("You do not have permission to edit this playlist.", "danger")
        return redirect(url_for('main.show_all_playlists'))

    # Use FlaskForm for input validation
    form = PlaylistForm(obj=playlist)  # Pre-fill form with current playlist data

    if form.validate_on_submit():
        try:
            # Update the playlist with validated form data
            playlist.name = form.name.data
            playlist.description = form.description.data
            db.session.commit()

            flash(f"Playlist '{playlist.name}' has been updated.", "success")
            return redirect(url_for('main.show_all_playlists'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the playlist. Please try again.", "danger")
            current_app.logger.error(f"Error updating playlist {playlist_id}: {e}")

    elif request.method == "POST":
        flash("There were errors in your form submission. Please fix them and try again.", "danger")

    return render_template('edit_playlist.html', playlist=playlist, form=form)




# debug for CSRF tokens
@main_bp.before_app_request
def log_request_details():
    current_app.logger.debug(f"Request: {request.method} {request.url}")
    if request.method == "POST":
        current_app.logger.debug(f"Form data: {request.form}")
