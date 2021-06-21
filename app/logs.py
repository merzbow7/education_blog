import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from pathlib import Path

from app import app

# ----- # ----- logging section  ----- # ----- #
if app.config['PROJECT_LOGGING_EMAIL']:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Ошибка',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

if app.config['PROJECT_LOGGING_FILE']:
    path_dir_log = Path(app.root_path) / "logs"
    if not path_dir_log.exists():
        path_dir_log.mkdir()
    file_handler = RotatingFileHandler('../logs/blog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    if not app.debug:
        app.logger.info('flask blog startup')