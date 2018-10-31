import psycopg2
import psycopg2.extras
from .database_models import DatabaseConnection
from dbConfig import config



class UserModel(DatabaseConnection):
    """Creates user object"""

    def __init__(self, email=None, password=None, role=None):
        super().__init__()
        self.email = email
        self.password = password
        self.role = role
        self.user_id = None
        db = DatabaseConnection()
        db.create_db_tables()

    def create_attendant_user(self):
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "INSERT INTO users(email,password,role) VALUES(%s,%s, 'attendant')", (
                self.email, self.password,)
        )
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (self.email,))
        row_result = cursor.fetchone()
        self.user_id = row_result[0]
        self.conn.commit()
        self.conn.close()

    def create_admin_user(self):
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
        self.conn.close()

    def create_default_admin(self):
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "INSERT INTO users(email, password, role) VALUES('allan@gmail.com', 'allangmailcompany', 'admin')"
        )
        self.conn.commit()
        self.conn.close()

    def get_all_users(self):
        """Fetches all users from the database"""
        db = DatabaseConnection()
        db.create_db_tables()
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
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        command = "SELECT * FROM users where user_id = {}".format(user_id)
        cursor.execute(command)
        user = cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        user_dict = {
            "user_id": user[0],
            "email": user[1],
            "password": user[2],
            "role": user[3]
        }
        return user_dict

    @staticmethod
    def get_role_by_email(email):
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * from users where email = '{}' ".format(email))
        role = cursor.fetchone()
        conn.commit()
        conn.close()
        return role

    def make_admin(self, user_id):
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "UPDATE users SET role = 'admin' WHERE user_id = {}".format(user_id)
        )
        self.conn.commit()
        self.conn.close()

    def blacklist_token(self, token):
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("Insert into blacklist(token) values(%s)", (token,))
        self.conn.commit()
        self.conn.close()

    def check_token(self, token):
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("Select * from blacklist where token = %s", (token,))
        exp_token = cursor.fetchone()
        self.conn.commit()
        return exp_token
