"""Forms"""

from flask_wtf.form import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import InputRequired

from app.validations import validate_not_common, validate_password, validate_username

class PasswordForm(FlaskForm):
    """Signup Form"""

    new_password = PasswordField(
        'New Password',
        [
            InputRequired(), 
            validate_password,
            validate_not_common
        ]
        # TODO: add validator to ensure password good
    )

    verified_password = PasswordField(
        'Verify Password',
        [InputRequired()]
    )

    submit = SubmitField('Change Password')

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField(
        'User Name',
        [InputRequired()]
    )

    password = PasswordField(
        'Password',
        [InputRequired()]
    )

    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    """Signup Form"""

    username = StringField(
        'User Name',
        [InputRequired(), validate_username]
    )

    password = PasswordField(
        'Password',
        [InputRequired(), validate_password]
    )

    submit = SubmitField('SignUp')
