from pathlib import Path
from flask import Flask, request, session, g

from flask_babel import Babel
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_security.models import fsqla_v2 as fsqla
from flask_sqlalchemy import SQLAlchemy

from settings import Configuration

app = Flask("__name__")
base_dir = Path(__file__).parent
app.template_folder = base_dir / "templates"
app.static_folder = base_dir / "static"
app.config.from_object(Configuration)
babel = Babel(app)

db = SQLAlchemy(app)
fsqla.FsModels.set_db_info(db)
migrate = Migrate(app, db)

mail = Mail(app)
moment = Moment(app)


@babel.localeselector
def get_locale():
    return session.get("lang", request.accept_languages.best_match(app.config['LANGUAGES']))
