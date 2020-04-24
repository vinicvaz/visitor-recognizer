from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import email_validator


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6, max=80)])


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])

    username = StringField('Username', validators=[
        InputRequired(), Length(min=4, max=15)])

    password = PasswordField('Password', validators=[
        InputRequired(), Length(min=6, max=80)])

    password2 = PasswordField('Confirm Password', validators=[
        InputRequired(), Length(min=6, max=80)])
