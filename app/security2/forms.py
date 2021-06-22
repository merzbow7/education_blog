from flask_babel import lazy_gettext as _l
from flask_security import RegisterForm, current_user

from wtforms import StringField
from wtforms.validators import DataRequired, StopValidation


class UniqueUserNameRequired(object):
    """
    Validate that username not in db.
    """
    field_flags = ('required',)

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = _l('Username already exist')

    def __call__(self, form, field):
        print(f'pre field data: {field.data}')
        if field.data:
            print(f'field data: {field.data}')
            if current_user.is_name_exist(field.data):
                raise StopValidation(self.message)


class ExtendedRegisterForm(RegisterForm):
    username = StringField(_l('Username'), [DataRequired(), UniqueUserNameRequired()])
