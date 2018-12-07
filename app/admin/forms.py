from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    TextAreaField,
    FileField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length
)
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app import db
from app.models import Role, User, Category

photos = UploadSet('photos', IMAGES)


class ChangeUserEmailForm(Form):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(Form):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class InviteUserForm(Form):
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
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
        ])
    password2 = PasswordField(
        'Confirm password',
        validators=[
            InputRequired(),
            EqualTo('password', 'Passwords must match.')
        ])

    submit = SubmitField('Create')


class AddCountryForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(1, 64)])
    overview = TextAreaField('Overview', validators=[InputRequired()])
    climate = TextAreaField('Climate')
    image = FileField(validators=[FileAllowed(photos, u'Image only!')])
    best_time_to_visit = TextAreaField('Best Time To Visit')
    submit = SubmitField('Add')


class EditCountryForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(1, 64)])
    overview = TextAreaField('Overview', validators=[InputRequired()])
    climate = TextAreaField('Climate')
    image = FileField(validators=[FileAllowed(photos, u'Image only!')])
    best_time_to_visit = TextAreaField('Best Time To Visit')
    submit = SubmitField('Add')


class AddBirdForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(1, 64)])
    image = FileField(validators=[FileAllowed(photos, u'Image only!')])
    park = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    submit = SubmitField('Add')


class EditBirdForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(1, 64)])
    image_url = FileField(validators=[FileAllowed(photos, u'Image only!')])
    submit = SubmitField('Add')


class AddWildlifeForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(1, 64)])
    frequency = StringField('Frequency', validators=[InputRequired()])
    image = FileField(validators=[FileAllowed(photos, u'Image only!')])
    park = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    submit = SubmitField('Add')


class EditWildlifeForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(1, 64)])
    frequency = StringField('Frequency', validators=[InputRequired()])
    image = FileField(validators=[FileAllowed(photos, u'Image only!')])
    park = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    submit = SubmitField('Add')


class AddParkForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(1, 64)])
    climate = TextAreaField('Climate')
    image = FileField(validators=[FileAllowed(photos, u'Image only!')])
    best_time_to_visit = TextAreaField('Best Time To Visit')
    country = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    submit = SubmitField('Add')


class EditParkForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(1, 64)])
    climate = TextAreaField('Climate')
    image = FileField(validators=[FileAllowed(photos, u'Image only!')])
    best_time_to_visit = TextAreaField('Best Time To Visit')
    country = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    submit = SubmitField('Add')

class CategoryForm(Form):
    name = StringField('name', validators=[Length(min=2, max=80)])
    image = FileField(validators=[FileAllowed(photos, u'Image only!')])
    submit = SubmitField('save')

    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category is not None:
            raise ValidationError('This category has already been added')
