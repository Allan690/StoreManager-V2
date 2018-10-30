import psycopg2
from flask import abort
from werkzeug.security import generate_password_hash
from .database_models import DatabaseConnection
from dbConfig import config


class UserModel(DatabaseConnection):
    """Creates user object"""
    def __init__(self, email=None, password=None, role=None):
        super().__init__()
        self.email = email
        self.password = password
        self.role = role
        db = DatabaseConnection()
        db.create_db_tables()

    def create_attendant_user(self):
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        if self.role == "Admin":
            user = UserModel()
            users = user.get_all_users()
            for user in users:
                if user["role"] == "Admin" or user["role"] == "admin":
                    abort(401, "Admin already exists")
        cursor.execute(
            "INSERT INTO users(email,password,role) VALUES(%s,%s,%s)", (
                self.email, self.password, self.role,)
        )
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (self.email,))
        row_result = cursor.fetchone()
        self.user_id = row_result[0]
        self.conn.commit()
        self.conn.close()

    def create_admin_user(self):
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        password = generate_password_hash('as@dsDdz2a', method='sha256')
        cursor.execute(
            "INSERT INTO users(email, password, role) VALUES('allan@gmail.com', %s, 'Admin')",
            (password,)
        )
        cursor.execute("SELECT role FROM users WHERE email = 'lorna@gmail.com'")
        row_result = cursor.fetchone()
        self.user_id = row_result[0]
        self.conn.commit()
        self.conn.close()

    def get_all_users(self):
        """Fetches all users from the database"""
        db = DatabaseConnection()
        db.create_db_tables()
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        command = "SELECT * FROM users"
        cursor.execute(command)
        users = cursor.fetchall()
        all_users = []
        for user in users:
            users_list = list(user)
            single_user = {"user_id": users_list[0],
                           "email": users_list[1],
                           "password": users_list[2],
                           "role": users_list[3]
                           }
            all_users.append(single_user)
        return all_users

    def make_admin(self, user_id):
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE users SET role = 'Admin' WHERE id = %s", (user_id,)
        )
        self.conn.commit()
        self.conn.close()