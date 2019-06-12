from flask_wtf import Form
from wtforms import Form as NoCsrfForm
from wtforms.fields import (
    BooleanField,
    StringField,
    SubmitField,
    FloatField,
    PasswordField,
    IntegerField,
    DateField,
    SelectField,
    FieldList,
    TextAreaField,
    FormField,
    HiddenField,
    DecimalField,
    FloatField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from app.models import *
from flask_login import current_user
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import request, g

photos = UploadSet("photos", IMAGES)


class ActivityForm(NoCsrfForm):
    activity = StringField("activity", validators=[Length(min=2, max=80)])


class PlaceForm(NoCsrfForm):
    place = StringField("Place", validators=[Length(min=2, max=80)])


class ImageForm(NoCsrfForm):
    image = FileField(
        validators=[
            FileAllowed(photos, u"Image Only!"),
            FileRequired(u"Choose a file!"),
        ]
    )


class DayForm(NoCsrfForm):
    title = StringField("Title", validators=[DataRequired()])
    day_by_day = TextAreaField("Day By day", validators=[Length(min=20, max=2000)])


class ListingForm(Form):
    title = StringField("title", validators=[Length(min=2, max=100)])
    location = SelectField(validators=[DataRequired()], choices=[], id="list-location")
    duration = SelectField(
        validators=[DataRequired()],
        coerce=int,
        choices=[(row, row) for row in range(1, 31)],
    )
    availability_from = DateField("availability_from", format="%d/%m/%Y")
    availability_to = DateField("availability_to", format="%d/%m/%Y")
    categories = SelectMultipleField(
        validators=[DataRequired()], choices=[], coerce=int, id="category-id"
    )
    physical_condition = SelectField(
        validators=[DataRequired()],
        choices=[
            ("Normal physcial condition", "Normal physcial condition"),
            (
                "Not fit for people with special conditions",
                "Not fit for people with special conditions",
            ),
        ],
    )
    connectivity = SelectField(
        validators=[DataRequired()],
        choices=[("Good", "Good"), ("Fair", "Fair"), ("Bad", "Bad")],
    )
    package = SelectField(
        validators=[DataRequired()],
        choices=[("Budget", "Budget"), ("Luxury", "Luxury")],
    )
    submit = SubmitField("save")


class ExtrasForm(Form):
    long_description = TextAreaField(
        "long description", validators=[Length(min=20, max=2000)]
    )
    activities = FieldList(
        FormField(ActivityForm, default=lambda: Activity()), min_entries=1
    )
    places = FieldList(FormField(PlaceForm, default=lambda: Place()), min_entries=1)
    days = FieldList(FormField(DayForm, default=lambda: Day()), min_entries=1)
    add_ons = TextAreaField("long description", validators=[Length(min=0, max=2000)])


class PolicyForm(Form):
    policy = TextAreaField("policy", validators=[Length(min=2, max=2000)])


class ImageForm(Form):
    images = FieldList(FormField(ImageForm), min_entries=1)


class EditListingForm(Form):
    title = StringField("title", validators=[Length(min=2, max=100)])
    location = SelectField(validators=[DataRequired()], choices=[], id="list-location")
    duration = SelectField(
        validators=[DataRequired()],
        coerce=int,
        choices=[(row, row) for row in range(1, 31)],
    )
    availability_from = DateField("availability_from", format="%d/%m/%Y")
    availability_to = DateField("availability_to", format="%d/%m/%Y")
    categories = SelectMultipleField(
        validators=[DataRequired()], choices=[], coerce=int, id="category-id"
    )
    physical_condition = SelectField(
        validators=[DataRequired()],
        choices=[
            ("Normal physcial condition", "Normal physcial condition"),
            (
                "Not fit for people with special conditions",
                "Not fit for people with special conditions",
            ),
        ],
    )
    connectivity = SelectField(
        validators=[DataRequired()],
        choices=[("Good", "Good"), ("Fair", "Fair"), ("Bad", "Bad")],
    )
    package = SelectField(
        validators=[DataRequired()],
        choices=[("Budget", "Budget"), ("Luxury", "Luxury")],
    )
    submit = SubmitField("save")


class CategoryForm(Form):
    name = StringField("name", validators=[Length(min=2, max=80)])
    image = FileField(validators=[FileAllowed(photos, u"Image only!")])
    submit = SubmitField("save")

    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category is not None:
            raise ValidationError("This category has already been added")


class IncludesForm(NoCsrfForm):
    include = StringField("Name", validators=[Length(min=2, max=80)])


class PriceForm(Form):
    total_price_adults = DecimalField(validators=[DataRequired()])
    total_price_children = DecimalField(validators=[DataRequired()])
    price_per_day_children = DecimalField(validators=[DataRequired()])
    price_per_day_adults = DecimalField(validators=[DataRequired()])
    includes = FieldList(FormField(IncludesForm), min_entries=1)


class EditPriceForm(Form):
    name = StringField("name", validators=[Length(min=2, max=100)])
    location = SelectField(validators=[DataRequired()], choices=[])
    total_price_adults = DecimalField(validators=[DataRequired()])
    total_price_children = DecimalField(validators=[DataRequired()])
    price_per_day_children = DecimalField(validators=[DataRequired()])
    price_per_day_adults = DecimalField(validators=[DataRequired()])
    includes = FieldList(
        FormField(IncludesForm, default=lambda: Include()), min_entries=1
    )


class MessageForm(Form):
    message = TextAreaField(
        "Message", validators=[DataRequired(), Length(min=0, max=140)]
    )
    submit = SubmitField("Submit")


class PhoneForm(NoCsrfForm):
    phone_number = StringField("phone_number", validators=[Length(min=2, max=80)])


class EmailForm(NoCsrfForm):
    email = StringField("phone_number", validators=[Length(min=2, max=80), Email()])


class LocationForm(NoCsrfForm):
    city = StringField("city", validators=[Length(min=2, max=100)])
    country = StringField("country", validators=[Length(min=2, max=100)])


class ProfileForm(Form):
    company_name = StringField("name", validators=[Length(min=2, max=100)])
    physical_address = StringField(validators=[Length(min=1, max=100)])
    postal_address = StringField(validators=[Length(min=1, max=100)])
    association_membership = StringField(validators=[Length(min=0, max=100)])
    overview = TextAreaField(validators=[Length(min=2, max=2000)])
    phones = FieldList(FormField(PhoneForm), min_entries=1)
    emails = FieldList(FormField(EmailForm), min_entries=1)
    locations = FieldList(FormField(LocationForm), min_entries=1)
    terms_of_use = BooleanField(validators=[DataRequired()], id="terms_of_use")
    operator_licence = FileField(
        validators=[
            FileAllowed(photos, u"Image Only!"),
            FileRequired(u"Choose a file!"),
        ]
    )
    reg_certificate = FileField(
        validators=[
            FileAllowed(photos, u"Image Only!"),
            FileRequired(u"Choose a file!"),
        ]
    )
    tax_registration = FileField(
        validators=[
            FileAllowed(photos, u"Image Only!"),
            FileRequired(u"Choose a file!"),
        ]
    )


class EditProfileForm(Form):
    company_name = StringField("name", validators=[Length(min=2, max=100)])
    overview = TextAreaField(validators=[Length(min=2, max=2000)])
    phones = FieldList(FormField(PhoneForm, default=lambda: Pubphones()), min_entries=1)
    emails = FieldList(FormField(EmailForm, default=lambda: Pubemails()), min_entries=1)
    locations = FieldList(
        FormField(LocationForm, default=lambda: Publocations()), min_entries=1
    )
    physical_address = StringField(validators=[Length(min=1, max=100)])
    postal_address = StringField(validators=[Length(min=1, max=100)])
    association_membership = StringField(validators=[Length(min=0, max=100)])
    terms_of_use = BooleanField(validators=[DataRequired()], id="terms_of_use")
    operator_licence = FileField(
        validators=[
            FileAllowed(photos, u"Image Only!"),
            FileRequired(u"Choose a file!"),
        ]
    )
    reg_certificate = FileField(
        validators=[
            FileAllowed(photos, u"Image Only!"),
            FileRequired(u"Choose a file!"),
        ]
    )
    tax_registration = FileField(
        validators=[
            FileAllowed(photos, u"Image Only!"),
            FileRequired(u"Choose a file!"),
        ]
    )


class BannerForm(Form):
    logo = FileField(validators=[FileAllowed(photos, u"Image only!")])
    banner = FileField(validators=[FileAllowed(photos, u"Image only!")])


class EditPasswordForm(Form):
    oldpassword = PasswordField("Password", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Save")

    def validate_oldpassword(self, oldpassword):
        user = User.query.filter_by(id=current_user.id).first()
        if user is None or not user.verify_password(oldpassword.data):
            raise ValidationError("Please enter correct Password.")
        return


class ListingForms(Form):
    location = SelectField(validators=[DataRequired()], choices=[], id="list-location")
    price_type_id = SelectField(
        validators=[DataRequired()], choices=[], coerce=int, id="list-package"
    )
    package = SelectField(
        validators=[DataRequired()],
        choices=[("Budget", "Budget"), ("Luxury", "Luxury")],
    )
    duration = StringField("duration", validators=[Length(min=2, max=80)])
    availability_from = DateField("availability_from", format="%d/%m/%Y")
    availability_to = DateField("availability_to", format="%d/%m/%Y")
    categories = SelectMultipleField(
        validators=[DataRequired()], choices=[], coerce=int
    )
    long_description = TextAreaField(
        "long description", validators=[Length(min=20, max=2000)]
    )
    activities = FieldList(FormField(ActivityForm), min_entries=1)
    places = FieldList(FormField(PlaceForm), min_entries=1)
    days = FieldList(FormField(DayForm), min_entries=1)
    images = FieldList(FormField(ImageForm), min_entries=1)
    physical_condition = StringField(
        "physical condition", validators=[Length(min=2, max=80)]
    )
    connectivity = StringField("Connectivity", validators=[Length(min=2, max=80)])
    add_ons = TextAreaField("long description", validators=[Length(min=0, max=2000)])
    policy = TextAreaField("policy", validators=[Length(min=2, max=2000)])
    submit = SubmitField("save")
