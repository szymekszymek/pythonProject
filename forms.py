from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField(' Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField(' Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UploadForm(FlaskForm):
    sep = SelectField('Delimiter', choices=[',', ';'])
    enc = SelectField('Encoding', choices=['utf-8', 'latin-1'])
    submit = SubmitField('Save')
