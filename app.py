from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager
from flask_security.models import fsqla_v2 as fsqla


from settings import Configuration

app = Flask("__name__")
app.config.from_object(Configuration)

# ----- # ----- Flask Manager section  ----- # ----- #
db = SQLAlchemy(app)
fsqla.FsModels.set_db_info(db)
migrate = Migrate(app, db)
manager = Manager(app)



