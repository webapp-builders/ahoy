from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextField,SelectField
from wtforms.validators import Required, Email,Length,Regexp,NumberRange,InputRequired


class ReminderForm(Form):
    reminder = StringField('reminder',validators=[InputRequired("Text required"),Length(1,120)])

