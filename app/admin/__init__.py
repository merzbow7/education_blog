from flask import Blueprint

bp = Blueprint('administrator', __name__)

from app.admin.api import AdminIndex, UserModelView, RoleModelView, PostModelView, CommentModelView
