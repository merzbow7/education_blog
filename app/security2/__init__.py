from flask import Blueprint

bp = Blueprint('security2', __name__)

from app.security2.forms import ExtendedRegisterForm, UniqueUserNameRequired
