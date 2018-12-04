from flask import url_for
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    DateField,
    DecimalField,
    SelectField,
    HiddenField,
    IntegerField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, DataRequired

from app.models import User
from app.models import *


class Search(Form):

    destinations = StringField('Destinations')
    kids = DecimalField('Kids')
    adults = DecimalField('Adults')
    check_in = DateField('Check In', format='%d/%m/%Y')
    check_out = DateField('Check Out', format='%d/%m/%Y')
    search = SubmitField('SEARCH NOW')


class BookingForm(Form):
    departure_date = DateField('Check In', validators=[DataRequired()], format='%m/%d/%Y')
    kids = IntegerField('Kids', validators=[DataRequired()])
    total = HiddenField(validators=[DataRequired()])
    adults = IntegerField('Adults', validators=[DataRequired()])
    book = SubmitField('BOOK NOW')


class PaymentForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    card_holder_name = StringField('Card Holder Name', validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired()])
    select_card  = SelectField('Select Card', validators=[DataRequired()], choices=[('1', 'EUR 6524 1254 6212 2541'), ('2', 'EUR 6524 1254 6212 2541'), ('3', 'USD 1254 6524 2541 6212')])
    month = SelectField(validators=[DataRequired()],
                        choices=[('jan', 'January'), ('feb', 'February'), ('mar', 'March'), ('apri', 'April')
                            , ('may', 'May'), ('jun', 'June'), ('jul', 'July'), ('aug', 'August'),
                                 ('sep', 'September'), ('octo', 'October'), ('nov', 'November'), ('dec', 'December')])
    years = SelectField(validators=[DataRequired()], choices=[('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022')])

    # card_identification_number =  StringField('Card Identification Number', validators=[DataRequired()])
    billing_zip_code =  StringField('Billing Zip Code', validators=[DataRequired()])

    confirm_booking = SubmitField('Confirm Booking')
