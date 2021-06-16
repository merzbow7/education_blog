from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, StopValidation

from flask_security import RegisterForm
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
        if User.query.filter_by(username=field.data).count():
            raise StopValidation(self.message)


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [DataRequired(), UniqueUserNameRequired()])


class ProfileForm(FlaskForm):
    username = StringField('Имя пользователя:', [DataRequired(), UniqueUserNameRequired()])
    file = FileField('Загрузите фото:', [FileRequired(), FileAllowed(['jpg', 'png', 'png'], 'Images only!')])
    button = SubmitField("Применить")


class AddNewPostForm(FlaskForm):
    title = StringField("Заголовок:", validators=[DataRequired()])
    post = TextAreaField("Новая запись:", validators=[DataRequired()])
    button = SubmitField("Добавить")


class AddCommentForm(FlaskForm):
    comment = TextAreaField("Ваш комментарий:", validators=[DataRequired()])
    button = SubmitField("Добавить")
