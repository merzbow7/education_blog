from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_babelex import lazy_gettext as _l
from app.security2 import UniqueUserNameRequired

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, StopValidation, Length


class FormDataRequired(object):
    """
    Validate form for some data
    """
    field_flags = ('required',)

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = _l('You must fill in at least one field')

    def __call__(self, form, field):
        is_data = False
        skipped = ['button', 'csrf_token']
        for field_form in form:
            if field_form.id not in skipped and field_form.data:
                is_data = True
        if not is_data:
            raise StopValidation(self.message)


class ProfileForm(FlaskForm):
    username = StringField(_l('Username'), [UniqueUserNameRequired()])
    about = TextAreaField(_l('About'), [Length(0, 255)])
    file = FileField(_l('Add image'), [FileAllowed(['jpg', 'png', 'png'], _l('Images only!'))])
    button = SubmitField(_l('Apply'), [FormDataRequired()])


class AddNewPostForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(1, 50)])
    post = TextAreaField(_l('New post'), validators=[DataRequired()])
    button = SubmitField(_l('Submit'))


class AddCommentForm(FlaskForm):
    comment = TextAreaField(_l('Your comment'), validators=[DataRequired()])
    button = SubmitField(_l('Submit'))
