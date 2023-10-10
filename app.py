"""Flask app for Notes"""

import os

from flask import Flask, redirect, render_template, session

from models import db, connect_db, User

from forms import RegisterNewUserForm, LoginForm, CSRFProtectForm


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "nibblers"

connect_db(app)


@app.get("/")
def get_registration_page():
    ''' Sends the user to the register page'''

    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def handle_registration_form():
    ''' Gets the user registrations form
        Handles creation of new user on submit '''

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

        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Produce login form and handle login"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = username
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Invalid username or password"]

    return render_template("login.html", form=form)


@app.get("/users/<username>")
def get_user_info_page(username):
    ''' Gets a a page with info about a specific user
        Only visible by that user '''

    if (session["username"] == username):

        user = User.query.get_or_404(username)
        return render_template(
            "user_page.html",
            user=user,
            form=CSRFProtectForm())

    elif (session["username"]):

        return redirect(f"/users/{username}")

    else:

        return redirect("/register")


@app.post("/logout")
def logout():
    ''' Logs the user out
        Redirects to the root route '''

    form = CSRFProtectForm()

    if form.validate_on_submit():

        session.pop("username", None)

    return redirect("/login")
