from flask import render_template, request, current_app
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.warning(f"cant resolve url: {request.url}")
    return render_template('errors/error.html', error=404), 404


@bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error(f"internal error: {error}")
    return render_template('errors/error.html', error=500), 500
