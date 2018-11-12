from sys import modules
from dbConfig import config, test_config
import psycopg2


class Configs(object):
    """This class defines the configurations for testing and
    normal/production environment"""

    def __init__(self):
        self.conn = None
        self.cur = None

    def test_configs(self):
        """Loads the test configurations"""
        if 'pytest' in modules or 'nosetests' in modules:
            params = test_config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()

    def normal_configs(self):
        """Loads the normal configurations"""
        params = config()
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()
