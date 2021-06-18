from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, StopValidation, ValidationError

from flask_security import RegisterForm, current_user
from models import User


class UniqueUserNameRequired(object):
    """
    Validate that username not in db.
    """
    field_flags = ('required',)

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = "Username is already exist."

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
            self.message = "Form is empty!"

    def __call__(self, form, field):
        is_data = False
        skipped = ["button", "csrf_token"]
        for field_form in form:
            if field_form.id not in skipped and field_form.data:
                is_data = True
        if not is_data:
            raise StopValidation(self.message)


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [DataRequired(), UniqueUserNameRequired()])


class ProfileForm(FlaskForm):
    username = StringField('Имя пользователя:')
    about = TextAreaField("О себе:")
    file = FileField('Загрузите фото:', [FileAllowed(['jpg', 'png', 'png'], 'Images only!')])
    button = SubmitField("Применить", [FormDataRequired()])


class AddNewPostForm(FlaskForm):
    title = StringField("Заголовок:", validators=[DataRequired()])
    post = TextAreaField("Новая запись:", validators=[DataRequired()])
    button = SubmitField("Добавить")


class AddCommentForm(FlaskForm):
    comment = TextAreaField("Ваш комментарий:", validators=[DataRequired()])
    button = SubmitField("Добавить")
