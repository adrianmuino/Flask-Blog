from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

USR_MIN_LEN = 2
USR_MAX_LEN = 20
EMAIL_MAX_LEN = 120
PASSWD_MIN_LEN = 8
PASSWD_MAX_LEN = 40
PASSWD_HASH_LEN = 60
FILENAME_LEN = 20

class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=USR_MIN_LEN, max=USR_MAX_LEN)])
    email = StringField("Email",
                        validators=[DataRequired(), Email(), Length(max=EMAIL_MAX_LEN)])
    password = PasswordField("Password",
                           validators=[DataRequired(), Length(min=PASSWD_MIN_LEN, max=PASSWD_MAX_LEN)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), Length(min=PASSWD_MIN_LEN, max=PASSWD_MAX_LEN), EqualTo('password')])
    sign_up = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=USR_MIN_LEN, max=USR_MAX_LEN)])
    password = PasswordField("Password",
                           validators=[DataRequired(), Length(min=PASSWD_MIN_LEN, max=PASSWD_MAX_LEN)])
    # Browser login cookie
    remember_me = BooleanField("Remember Me")

    log_in = SubmitField("Log In")