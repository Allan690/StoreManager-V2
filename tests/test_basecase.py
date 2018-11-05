import unittest
from app import flask_app
from app.api.v2.models.database_models import DatabaseConnection
from app.api.v2.models.user_models import UserModel
db_obj = DatabaseConnection()
user_obj = UserModel()


class TestSetUp(unittest.TestCase):
    """Initialize the app with test data"""
    def setUp(self):
        self.app = flask_app.test_client()
        db_obj.create_db_tables()
        user_obj.create_default_admin()

    def tearDown(self):
            db = DatabaseConnection()
            db.destroy_tables()
            db.create_db_tables()


