from app.api.v2.models.user_models import UserModel

user = UserModel()

user.create_db_tables()
user.create_default_admin()
