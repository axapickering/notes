"""Forms for users"""


from wtforms import IntegerField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, Length, Email

class RegisterNewUserForm(FlaskForm):

    username = StringField("Username:",validators=[InputRequired(),Length(max=20)])

    password = PasswordField("Password:",validators=[InputRequired(),Length(max=100)])

    email = StringField("Email:",validators=[InputRequired(),Length(max=50),Email()])

    first_name = StringField("First name:",validators=[InputRequired(),Length(max=30)])

    last_name = StringField("Last name:",validators=[InputRequired(),Length(max=30)])



