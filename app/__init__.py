import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from pathlib import Path

from flask import Flask, request, session, current_app, url_for
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from flask_babelex import Babel
from settings import Configuration
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.models import fsqla_v2 as fsqla

from app.admin import AdminIndex, UserModelView, RoleModelView, PostModelView, CommentModelView
from app.security2 import ExtendedRegisterForm

db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='Merzbow', template_mode='bootstrap4')
security = Security()
mail = Mail()
moment = Moment()
babel = Babel()


def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    fsqla.FsModels.set_db_info(db)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)

    babel.init_app(app)

    from app.models import User, Role, Comment, Post

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)

    admin.init_app(app=app, url='/admin', index_view=AdminIndex())

    admin.add_views(UserModelView(User, db.session),
                    RoleModelView(Role, db.session),
                    CommentModelView(Comment, db.session),
                    PostModelView(Post, db.session), )

    admin.add_link(MenuLink(name='Blogs', category='', url='/'))

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if app.config['PROJECT_LOGGING_EMAIL'] and not app.config["TESTING"]:
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

    if app.config['PROJECT_LOGGING_FILE'] and not app.config["TESTING"]:
        path_dir_log = Path(app.root_path) / "logs"
        file_log = path_dir_log / "blog.log"
        if not path_dir_log.exists():
            path_dir_log.mkdir()
        file_handler = RotatingFileHandler(file_log, maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        if not app.debug:
            app.logger.info('flask blog startup')

    return app


@babel.localeselector
def get_locale():
    return session.get("lang", request.accept_languages.best_match(current_app.config['LANGUAGES']))
