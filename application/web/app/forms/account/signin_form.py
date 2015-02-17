from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextField,SelectField
from wtforms.validators import Required, Email,Length,Regexp,NumberRange,InputRequired
from wtforms.fields.html5 import EmailField



class SigninForm(Form):
    password = PasswordField('Password',validators=[InputRequired("Password is required"),Length(6,100,"Password must be between 6 and 100 characters long")])
    email = StringField('Email',validators=[InputRequired("Email is required"),Length(1,120),Email()])
