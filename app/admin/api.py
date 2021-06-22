from flask import request, redirect, abort, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user


class AccessModelView:
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
                )

    def _handle_view(self, name, **kwargs):
        """
            Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class BaseAdminModelView(AccessModelView, ModelView):
    pass


class AdminIndex(AccessModelView, AdminIndexView):
    pass


class PostModelView(BaseAdminModelView):
    column_list = ('title', 'body', 'user.username')
    form_columns = ('user_id', 'hash_name', 'title', 'body')


class UserModelView(BaseAdminModelView):
    column_list = ['email', 'active', 'roles']
    form_columns = ['email', 'active', 'roles']


class RoleModelView(BaseAdminModelView):
    column_list = ["name", "description"]


class CommentModelView(BaseAdminModelView):
    column_list = ('body', 'user.username')
    form_columns = ['body']
