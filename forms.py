from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import Email, Length, DataRequired, EqualTo


class AddNewPostForm(FlaskForm):
    title = StringField("Заголовок:", validators=[DataRequired()])
    post = TextAreaField("Новая запись:", validators=[DataRequired()])
    button = SubmitField("Добавить")


class AddCommentForm(FlaskForm):
    comment = TextAreaField("Комментарий:", validators=[DataRequired()])
    button = SubmitField("Добавить")
