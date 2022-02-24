import os
from flask_migrate import Migrate
#from flask_script import Manager
from flask_admin import Admin

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security

from flask_app_init import app, db

MIGRATION_DIR = os.path.join('admin', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)
#manager = Manager(app)


# FLASK-ADMIN
from models import User, Role, Product, Commission
from views import HomeAdminView, ProductView, LogoutView, CommView

admin = Admin(app, 'KaspiParse', url='/admin', index_view=HomeAdminView())
admin.add_view(ProductView(Product, db.session))
admin.add_view(CommView(Commission, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='admin/logout_redirect'))

# FLASK-SECURITY
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
