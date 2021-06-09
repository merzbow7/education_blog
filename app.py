from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager
from flask_security.models import fsqla_v2 as fsqla
from flask_security import SQLAlchemyUserDatastore, Security
import datetime

from settings import Configuration

app = Flask("__name__")
app.config.from_object(Configuration)

# ----- # ----- Flask Manager section  ----- # ----- #
db = SQLAlchemy(app)
fsqla.FsModels.set_db_info(db)
migrate = Migrate(app, db)
manager = Manager(app)

# ----- # ----- Flask Security section  ----- # ----- #

from models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
