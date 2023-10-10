"""Flask app for Notes"""

import os
from flask import Flask, redirect, render_template, session
from models import db, connect_db, User
from forms import RegisterNewUserForm, LoginForm, CSRFProtectForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "nibblers"

connect_db(app)
#TODO: make global var for session username

@app.get("/")
def home_page():
    ''' Sends the user to the register page'''

    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def handle_registration_form():
    ''' Gets the user registration form
        Handles creation of new user on submit '''

    #TODO: if user is already logged in, redirect to user's page

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
    """Produce login form or handle login"""

    #TODO: redirect if already logged in

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
    ''' Gets a page with info about a specific user
        Only visible by that user '''
    #TODO: raise a unauthorized flask error (401) import
    #raise Unauthorized
    #put guard at top
    #TODO: add flash messages


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
        Redirects to the login page '''

    #TODO: else: raise unauthorized

    form = CSRFProtectForm()

    if form.validate_on_submit():

        session.pop("username", None)

    return redirect("/login")
