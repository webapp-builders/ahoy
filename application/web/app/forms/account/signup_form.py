
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextField,SelectField
from wtforms.validators import Required, Email,Length,Regexp,NumberRange,InputRequired
from wtforms.fields.html5 import EmailField
#from app.models.user import User


class SignupForm(Form):
    username = StringField('Username',validators=[InputRequired("Username is required"),Length(1,100),
                Regexp('^[A-Za-z0-9-]{1,}$',message="only letters, numbers and dashes allowed")])
    password = PasswordField('Password',validators=[InputRequired("Password is required"),Length(6,100,"Password must be between 6 and 100 characters long")])
    email = StringField('Email',validators=[InputRequired("Email is required"),Length(1,120),Email()])

    # uncomment for explicit validation
    # instead just handle the rare case of database constraint violation email already exists
    # in that case capture:
    # IntegrityError: (IntegrityError) duplicate key value violates unique constraint "ix_users_email"
    # def validate_email(self,email_field):
    #     if User.get_by_email(email_field.data):
    #         raise ValidationError('There already is a user with this email address')
