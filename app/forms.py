from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_babel import lazy_gettext as _l
from flask_security import RegisterForm

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, StopValidation, Length

from app.models import User


class UniqueUserNameRequired(object):
    """
    Validate that username not in db.
    """
    field_flags = ('required',)

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = _l('Username already exists!')

    def __call__(self, form, field):
        if field.data:
            if User.query.filter_by(username=field.data).count():
                raise StopValidation(self.message)


class FormDataRequired(object):
    """
    Validate form for some data
    """
    field_flags = ('required',)

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = _l('Form is empty!')

    def __call__(self, form, field):
        is_data = False
        skipped = ['button', 'csrf_token']
        for field_form in form:
            if field_form.id not in skipped and field_form.data:
                is_data = True
        if not is_data:
            raise StopValidation(self.message)


class ExtendedRegisterForm(RegisterForm):
    username = StringField(_l('Username'), [DataRequired(), UniqueUserNameRequired()])


class ProfileForm(FlaskForm):
    username = StringField(_l('Username'), [Length(1, 25)])
    about = TextAreaField(_l('About'), [Length(1, 255)])
    file = FileField(_l('Add image'), [FileAllowed(['jpg', 'png', 'png'], _l('Images only!'))])
    button = SubmitField(_l('Apply'), [FormDataRequired()])


class AddNewPostForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(1, 50)])
    post = TextAreaField(_l('New post'), validators=[DataRequired()])
    button = SubmitField(_l('Submit'))


class AddCommentForm(FlaskForm):
    comment = TextAreaField(_l('Your comment'), validators=[DataRequired()])
    button = SubmitField(_l('Submit'))
