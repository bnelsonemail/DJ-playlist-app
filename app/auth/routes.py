"""app/auth/routes.py"""

from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required
from app.models import db, User
from app.forms import LoginForm, RegistrationForm
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        current_app.logger.debug("Form validation succeeded.")
        
        # Log the email being queried
        current_app.logger.debug(f"Looking up user with email: {form.email.data}")
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            current_app.logger.debug(f"User found: {user}")
            
            # Log password check
            if user.check_password(form.password.data):
                current_app.logger.debug("Password matched.")
                login_user(user)
                flash("Logged in successfully!", "success")  # Added message required for the test case
                return redirect(url_for('main.show_all_playlists'))

            else:
                current_app.logger.debug("Invalid password.")
        else:
            current_app.logger.debug(f"No user found with email: {form.email.data}")
        
        flash("Invalid email or password.", "danger")
    else:
        if request.method == 'POST':
            current_app.logger.debug(f"Form validation failed: {form.errors}")

    # Always return the rendered template if no redirect happens
    return render_template('login.html', form=form)






@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration page."""
    form = RegistrationForm()
    current_app.logger.debug("Accessed registration page.")

    if request.method == "POST":
        current_app.logger.debug(f"Request.form: {request.form}")
        current_app.logger.debug("Form fields received:")
        current_app.logger.debug(f"Username: {form.username.data}")
        current_app.logger.debug(f"Email: {form.email.data}")
        current_app.logger.debug(f"Password: {form.password.data}")
        current_app.logger.debug(f"Confirm Password: {form.confirm_password.data}")

        if form.validate_on_submit():
            current_app.logger.debug("Form validation passed.")

            # Check for existing username
            existing_user_by_username = User.query.filter_by(username=form.username.data).first()
            current_app.logger.debug(f"Existing username result: {existing_user_by_username}")
            if existing_user_by_username:
                flash("Username already exists.", "danger")
                current_app.logger.debug("Username already exists.")
                return render_template("register.html", form=form)

            # Check for existing email
            existing_user_by_email = User.query.filter_by(email=form.email.data).first()
            current_app.logger.debug(f"Existing email result: {existing_user_by_email}")
            if existing_user_by_email:
                flash("Email already exists.", "danger")
                current_app.logger.debug("Email already exists.")
                return render_template("register.html", form=form)

            # Create the user
            try:
                user = User(
                    username=form.username.data,
                    email=form.email.data,
                )
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()

                flash("Account created successfully. Please log in.", "success")
                current_app.logger.debug(f"User created successfully: {user}")
                return redirect(url_for("auth.login"))
            except Exception as e:
                db.session.rollback()
                flash("An error occurred. Please try again.", "danger")
                current_app.logger.error(f"Error during user creation: {e}")
        else:
            # Log detailed validation errors
            current_app.logger.debug(f"Form validation failed: {form.errors}")
            flash("Please correct the errors in the form.", "danger")

    return render_template("register.html", form=form)






@auth_bp.route("/logout")
@login_required
def logout():
    """Log out the user."""
    print("Logout route accessed.")  # Debug statement
    print(f"Flash function: {flash}")  # Ensure flash is accessible
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))




