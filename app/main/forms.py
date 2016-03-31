from wtforms import Form, TextField, PasswordField, validators, SubmitField, StringField
from wtforms.validators import DataRequired, Length,  Regexp, EqualTo
from wtforms import ValidationError, validators, SubmitField
from views import User
from flask.ext.wtf import Form


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')], description="test")
    password_hash = PasswordField('password', validators=[DataRequired()])

    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            print "at validate"
            return True
        print "YESSS"
        user = User.query.filter_by(username=self.username.data.lower()).first()
        print "We are getting there"
        if user and user.verify_password(self.password_hash.data):
            print "hello world"
            return True

        else:
            self.username.errors.append("Invalid username or password")
            return False

