from flask_security import SQLAlchemyUserDatastore, Security
from app import app, db
from app.models import User, Role
from app.forms import ExtendedRegisterForm

# ----- # ----- Flask Security section  ----- # ----- #


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)
