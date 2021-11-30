from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User
import flaskblog.utils as utils

class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=utils.USR_MIN_LEN, max=utils.USR_MAX_LEN)])
    email = StringField("Email",
                        validators=[DataRequired(), Email(), Length(max=utils.EMAIL_MAX_LEN)])
    password = PasswordField("Password",
                           validators=[DataRequired(), Length(min=utils.PASSWD_MIN_LEN, max=utils.PASSWD_MAX_LEN)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), Length(min=utils.PASSWD_MIN_LEN, max=utils.PASSWD_MAX_LEN), EqualTo('password')])
    # Browser login cookie
    remember_me = BooleanField("Remember Me")
    sign_up = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=utils.USR_MIN_LEN, max=utils.USR_MAX_LEN)])
    password = PasswordField("Password",
                           validators=[DataRequired(), Length(min=utils.PASSWD_MIN_LEN, max=utils.PASSWD_MAX_LEN)])
    # Browser login cookie
    remember_me = BooleanField("Remember Me")

    log_in = SubmitField("Log In")

class AccountUpdateForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=utils.USR_MIN_LEN, max=utils.USR_MAX_LEN)])
    email = StringField("Email",
                        validators=[DataRequired(), Email(), Length(max=utils.EMAIL_MAX_LEN)])
    picture = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    update = SubmitField("Update")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user != current_user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user != current_user:
            raise ValidationError("That email is taken. Please choose a different one.")

class RequestResetForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email(), Length(max=utils.EMAIL_MAX_LEN)])
    request_reset = SubmitField("Request Password Reset")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("User with email {} does not exist. Please enter a registered email.".format(email))

class ResetForm(FlaskForm):
    password = PasswordField("Password",
                           validators=[DataRequired(), Length(min=utils.PASSWD_MIN_LEN, max=utils.PASSWD_MAX_LEN)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), Length(min=utils.PASSWD_MIN_LEN, max=utils.PASSWD_MAX_LEN), EqualTo('password')])
    reset = SubmitField("Reset Password")