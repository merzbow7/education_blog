from flask import render_template, request, current_app
from flask_babelex import _
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.warning(f"cant resolve url: {request.url}")
    error = {"number": 404,
             "name": _('Page Not Found'),
             "description": ""}
    return render_template('errors/error.html', error=error), 404


@bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error(f"internal error: {error}")
    error = {"number": 500,
             "name": _("Internal server error"),
             "description": ""}
    return render_template('errors/error.html', error=error), 500


@bp.app_errorhandler(403)
def forbidden(error):
    current_app.logger.error(f"forbidden: {error}")
    error = {"number": 403,
             "name": _("Forbidden"),
             "description": _("You do not have permission to access the requested resource")}
    return render_template('errors/error.html', error=error), 403
