import unittest
from app import flask_app
from app.api.v2.models.database_models import DatabaseConnection
db_obj = DatabaseConnection()


class TestSetUp(unittest.TestCase):
    """Initialize the app with test data"""
    def setUp(self):
        self.app = flask_app.test_client()
        db_obj.create_db_tables()

    def tearDown(self):
            db = DatabaseConnection()
            db.destroy_tables()
            db.create_db_tables()


