from flask_security import SQLAlchemyUserDatastore, Security
from app import app, db
from models import User, Role

# ----- # ----- Flask Security section  ----- # ----- #


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
