from flask import Flask

from flask_babel import Babel
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_script import Manager
from flask_security.models import fsqla_v2 as fsqla
from flask_sqlalchemy import SQLAlchemy

from settings import Configuration

app = Flask("__name__")
app.config.from_object(Configuration)

db = SQLAlchemy(app)
fsqla.FsModels.set_db_info(db)
migrate = Migrate(app, db)

babel = Babel(app)
mail = Mail(app)
manager = Manager(app)
moment = Moment(app)
