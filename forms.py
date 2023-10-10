"""Forms for users"""

from wtforms import StringField, PasswordField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email, Optional


####################### USER FORMS ############################

class RegisterNewUserForm(FlaskForm):
    """Form for registering a new user"""

    username = StringField(
        "Username:",
        validators=[InputRequired(), Length(min=4,max=20)]
    )

    password = PasswordField(
        "Password:",
        validators=[InputRequired(), Length(min=5,max=100)]
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

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )



####################### NOTE FORMS ############################

class EditNoteForm(FlaskForm):
    ''' Form allowing user to edit a note '''

    title = StringField(validators=[Optional(),Length(min=3,max=100)])

    content = TextAreaField(validators=[Optional(),Length(min=3)])


class AddNoteForm(FlaskForm):
    ''' Form allowing user to add a note '''

    title = StringField(validators=[InputRequired(),Length(min=3,max=100)])

    content = TextAreaField(validators=[InputRequired(),Length(min=3)])



####################### CSRF FORM ##############################


class CSRFProtectForm(FlaskForm):
    ''' For CSRF protection purposes'''
