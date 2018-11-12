from app import flask_app
from app.api.v2.models.database_models import DatabaseConnection
from app.api.v2.models.user_models import UserModel
# update the configurations of our application
flask_app.config.update(
    DEBUG=True
)
flask_app.secret_key = 'hello-there-its-allan'
if __name__ == '__main__':
    db = DatabaseConnection()
    db.create_db_tables()
    user = UserModel()
    user.create_default_admin()
    flask_app.run()
