from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=25, message='Username must be between 3 and 25 characters long')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    role_id = SelectField('Role', coerce=int, validators=[DataRequired(), NumberRange(min=1, max=9)])
    email = EmailField('Email', validators=[
        Length(min=5, max=50)
    ])

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    role_id = SelectField('Role', coerce=int, validators=[DataRequired()])
    name = StringField('Name')
    email = StringField('Email', validators=[Length(min=5, max=50)])
    status = StringField('Status', default='active')
    is_active = BooleanField('Active')
    password = PasswordField('New Password', validators=[
        Length(min=8),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm New Password')


class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    role = SelectField('Role', choices=[
        ('superuser', 'Superuser'),
        ('admin', 'Admin'),
        ('member', 'Member')
    ])
    submit = SubmitField('Add User')