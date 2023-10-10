"""Forms for users"""

from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email


class RegisterNewUserForm(FlaskForm):
    """Form for registering a new user"""

    username = StringField(
        "Username:",
        validators=[InputRequired(), Length(max=20)]
    )
    #TODO: add minimum
    password = PasswordField(
        "Password:",
        validators=[InputRequired(), Length(max=100)]
    )

    email = StringField(
        "Email:",
        validators=[InputRequired(), Length(max=50), Email()]
    )

    first_name = StringField(
        "First name:",
        validators=[InputRequired(), Length(max=30)]
    )

    last_name = StringField(
        "Last name:",
        validators=[InputRequired(), Length(max=30)]
    )


class LoginForm(FlaskForm):
    """Form for logging in a user"""
    #TODO: remove Lengths
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=100)]
    )


class CSRFProtectForm(FlaskForm):
    ''' For CSRF protection purposes'''
