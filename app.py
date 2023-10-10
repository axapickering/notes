"""Flask app for Notes"""

import os
from flask import Flask, redirect, render_template, session, flash
from models import db, connect_db, User
from forms import RegisterNewUserForm, LoginForm, CSRFProtectForm, EditNoteForm, AddNoteForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "nibblers"

connect_db(app)

USERNAME = "username"


@app.get("/")
def home_page():
    ''' Sends the user to the register page'''

    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def handle_registration_form():
    ''' Gets the user registration form
        Handles creation of new user on submit '''

    if (USERNAME in session):
        return redirect(f"/user/{session[USERNAME]}")

    form = RegisterNewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        flash("User successfully registered")

        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Produce login form or handle login"""

    if (USERNAME in session):
        return redirect(f"/user/{session[USERNAME]}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = username
            flash(f"User {username} successfully logged in")
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Invalid username or password"]

    return render_template("login.html", form=form)


@app.get("/users/<username>")
def get_user_info_page(username):
    ''' Gets a page with info about a specific user
        Only visible by that user '''

    if (USERNAME not in session or session[USERNAME] != username):

        raise Unauthorized()

    else:

        user = User.query.get_or_404(username)
        return render_template(
            "user_page.html",
            user=user,
            notes=user.notes,
            form=CSRFProtectForm())


@app.post("/logout")
def logout():
    ''' Logs the user out
        Redirects to the login page '''

    form = CSRFProtectForm()

    if form.validate_on_submit():

        session.pop("username", None)
        flash("Successfully logged out.")
        return redirect("/login")

    else:

        raise Unauthorized()

@app.post("/users/<username>/delete")
def delete_user(username):
    """Removes user from database, logs the user out and redirect to home page"""

    form = CSRFProtectForm()

    if (
        USERNAME not in session or
        session[USERNAME] != username or
        not form.validate_on_submit()
        ):

        raise Unauthorized()

    elif form.validate_on_submit():
        user = User.query.get_or_404(username)
        session.pop("username", None)
        db.session.delete(user.notes)
        db.session.delete(user)
        db.session.commit()

        flash("User successfully deleted.")
        redirect("/")



