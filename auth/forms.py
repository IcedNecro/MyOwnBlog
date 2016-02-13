from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
import models

class LoginForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])