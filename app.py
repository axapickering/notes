"""Flask app for Notes"""

import os

from flask import Flask, request, redirect, render_template, flash, jsonify

from models import db, connect_db, Cupcake, DEFAULT_IMAGE_URL

from forms import RegisterNewUserForm


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

@app.route("/register",methods=['GET','POST'])
def handle_registration_form():
    ''' Gets the user registrations form
        Handles creation of new user on submit '''

    form = RegisterNewUserForm()

    if form.validate_on_submit():



