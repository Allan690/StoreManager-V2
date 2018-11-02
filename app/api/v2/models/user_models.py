import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash

from .database_models import DatabaseConnection
from dbConfig import config, test_config
from sys import modules


class UserModel(DatabaseConnection):
    """Creates user object"""
    def __init__(self, email=None, password=None, role=None):
        super().__init__()
        self.email = email
        self.password = password
        self.role = role
        self.user_id = None

    def create_attendant_user(self):
        if 'pytest' in modules or 'nosetests' in modules:
            params = test_config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print(cursor)
            cursor.execute(
                "INSERT INTO users(email,password,role) VALUES(%s,%s, 'attendant')", (
                    self.email, self.password,)
            )
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (self.email,))
            row_result = cursor.fetchone()
            self.user_id = row_result[0]
            print(self.user_id)
            self.conn.commit()

        else:
            params = config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(
                "INSERT INTO users(email,password,role) VALUES(%s,%s, %s)", (
                    self.email, self.password, self.role,)
            )
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (self.email,))
            row_result = cursor.fetchone()
            self.user_id = row_result[0]
            self.conn.commit()

    def create_admin_user(self):
        if 'pytest' in modules or 'nosetests' in modules:
            params = test_config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(
                "INSERT INTO users(email, password, role) VALUES(%s, %s, 'admin')",
                (self.email, self.password,)
            )
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (self.email,))
            row_result = cursor.fetchone()
            self.user_id = row_result[0]
            self.conn.commit()

        else:
            params = config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(
                "INSERT INTO users(email, password, role) VALUES(%s, %s, 'admin')",
                (self.email, self.password,)
            )
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (self.email,))
            row_result = cursor.fetchone()
            self.user_id = row_result[0]
            self.conn.commit()

    def create_default_admin(self):
        if 'pytest' in modules or 'nosetests' in modules:
            params = test_config()
            self.conn = psycopg2.connect(**params)
            query = "SELECT * FROM users where email = 'allan@gmail.com'"
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
            res = cursor.fetchone()
            if not res:
                password_hash = generate_password_hash('allangmailcompany', method='sha256')
                cursor.execute(
                    "INSERT INTO users(email, password, role) VALUES('allan@gmail.com', %s, 'admin')", (password_hash,)
                )
            self.conn.commit()
        else:
            params = config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            password_hash = generate_password_hash('allangmailcompany', method='sha256')
            cursor.execute(
                "INSERT INTO users(email, password, role) VALUES('allan@gmail.com', %s, 'admin')"
                "on conflict(email) do nothing;", (password_hash,)
            )
            self.conn.commit()

    def get_all_users(self):
        """Fetches all users from the database"""
        if 'pytest' in modules or 'nosetests' in modules:
            self.create_default_admin()
            params = test_config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            command = "SELECT * FROM users"
            cursor.execute(command)
            users = cursor.fetchall()
            user_list = []
            self.conn.commit()
            for user in users:
                user_dict = {
                    "user_id": user[0],
                    "email": user[1],
                    "password": user[2],
                    "role": user[3]
                }
                user_list.append(user_dict)
            return user_list

        else:
            self.create_default_admin()
            params = config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            command = "SELECT * FROM users"
            cursor.execute(command)
            users = cursor.fetchall()
            user_list = []
            self.conn.commit()
            for user in users:
                user_dict = {
                    "user_id": user[0],
                    "email": user[1],
                    "password": user[2],
                    "role": user[3]
                }
                user_list.append(user_dict)
            return user_list

    def get_user_by_id(self, user_id):
        """Fetches a particular user from the database by supplied id"""
        if 'pytest' in modules or 'nosetests' in modules:
                params = test_config()
                self.conn = psycopg2.connect(**params)
                cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                command = "SELECT * FROM users where user_id = {}".format(user_id)
                cursor.execute(command)
                user = cursor.fetchall()
                self.conn.commit()
                user_dict = {
                    "user_id": user[0],
                    "email": user[1],
                    "password": user[2],
                    "role": user[3]
                }
                return user_dict
        else:
            params = config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            command = "SELECT * FROM users where user_id = {}".format(user_id)
            cursor.execute(command)
            user = cursor.fetchall()
            self.conn.commit()
            user_dict = {
                "user_id": user[0],
                "email": user[1],
                "password": user[2],
                "role": user[3]
            }
            return user_dict

    @staticmethod
    def get_user_by_email(email):
        if 'pytest' in modules or 'nosetests' in modules:
            params = test_config()
            conn = psycopg2.connect(**params)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * from users where email = '{}' ".format(email))
            user = cursor.fetchone()
            conn.commit()
            return user
        else:
            params = config()
            conn = psycopg2.connect(**params)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * from users where email = '{}' ".format(email))
            user = cursor.fetchone()
            conn.commit()
            return user

    def make_admin(self, user_id):
        if 'pytest' in modules or 'nosetests' in modules:
            params = test_config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(
                "UPDATE users SET role = 'admin' WHERE email = '{}'".format(user_id)
            )
            self.conn.commit()
        else:
            params = config()
            self.conn = psycopg2.connect(**params)
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(
                "UPDATE users SET role = 'admin' WHERE email = '{}'".format(user_id)
            )
            self.conn.commit()

