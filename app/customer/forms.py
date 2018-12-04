from flask import url_for
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextField,
    DateField,
    DecimalField,
    SelectField,
    TextAreaField
)
from wtforms import RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, DataRequired

from app.models import User
from app.models import *


class ReviewForm(Form):

    stars = RadioField('Label', coerce=int)
    comment = TextAreaField(
        'Comment', validators=[InputRequired(),
                               Length(1, 300)])
    submit = SubmitField('Submit')


class ProfileForm(Form):
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    address = StringField(
        'Address', validators=[InputRequired(),
                               Length(1, 64)])
    dob = DateField('D O B', validators=[DataRequired()], format='%d/%m/%Y')

    submit = SubmitField('Submit')
