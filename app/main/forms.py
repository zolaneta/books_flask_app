from wtforms import Form, TextField, PasswordField, validators, SubmitField, StringField
from wtforms.validators import DataRequired, Length,  Regexp, EqualTo
from wtforms import ValidationError, validators, SubmitField
from views import User
from flask.ext.wtf import Form


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')], description="test")
    password = PasswordField('password', validators=[DataRequired()])

    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data.lower()).first()
        if user and user.verify_password(self.password.data):
            return True

        else:
            self.username.errors.append("Invalid username or password")
            return False

