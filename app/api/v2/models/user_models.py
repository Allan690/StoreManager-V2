from werkzeug.security import generate_password_hash
from .database_models import DatabaseConnection


class UserModel(DatabaseConnection):
    """Creates user object"""
    def __init__(self, email=None, password=None, role=None):
        super().__init__()
        db = DatabaseConnection()
        self.email = email
        self.password = password
        self.role = role
        self.user_id = None
        self.cursor = db.cursor_obj()

    def create_attendant_user(self):
        """Creates an attendant user"""
        self.cursor.execute(
            "INSERT INTO users(email,password,role) VALUES(%s,%s, 'attendant')",
            (
                self.email, self.password,)
        )
        self.cursor.execute("SELECT user_id FROM users WHERE email = %s",
                            (self.email,))
        row_result = self.cursor.fetchone()
        self.user_id = row_result["user_id"]

    def create_admin_user(self):
        """Creates an admin user"""
        self.cursor.execute(
            "INSERT INTO users(email, password, role) VALUES(%s, %s, 'admin')",
            (self.email, self.password,)
        )
        self.cursor.execute("SELECT user_id FROM users WHERE email = %s",
                            (self.email,))
        row_result = self.cursor.fetchone()
        self.user_id = row_result["user_id"]

    def create_default_admin(self):
        """This method creates a default admin in the database"""
        query = "SELECT * FROM users where email = 'allan@gmail.com'"
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if not res:
            password_hash = generate_password_hash('allangmailcompany',
                                                   method='sha256')
            self.cursor.execute(
                "INSERT INTO users(email, password, role) "
                "VALUES('allan@gmail.com', %s, 'admin')", (password_hash,)
            )

    def get_all_users(self):
        """Fetches all users from the database"""
        command = "SELECT * FROM users"
        self.cursor.execute(command)
        users = self.cursor.fetchall()
        return users

    def get_all_attendants(self):
        """Fetches all attendant users"""
        command = "SELECT * FROM users where role= 'attendant'"
        self.cursor.execute(command)
        users = self.cursor.fetchall()
        return users

    def get_admin_users(self):
        """Fetches all admin users"""
        command = "SELECT * FROM users where role= 'admin'"
        self.cursor.execute(command)
        users = self.cursor.fetchall()
        return users

    def get_user_by_id(self, user_id):
        """Fetches a particular user from the database by supplied id"""
        command = "SELECT * FROM users where user_id = {}".format(user_id)
        self.cursor.execute(command)
        user = self.cursor.fetchall()
        return user

    @staticmethod
    def get_user_by_email(email):
        """Gets a user by supplied email address"""
        user = UserModel()
        user.cursor.execute("SELECT * from users where email = '{}' ".format
                            (email))
        user1 = user.cursor.fetchone()
        return user1

    @staticmethod
    def get_attendant_by_email(email):
        """Gets an attendant user by supplied email"""
        user = UserModel()
        user.cursor.execute("SELECT * from users where email = '{}' and "
                            "role ='attendant' ".format(email))
        user1 = user.cursor.fetchone()
        return user1

    def make_admin(self, user_id):
        """This method makes an attendant user admin"""
        self.cursor.execute(
            "UPDATE users SET role = 'admin' WHERE email = '{}'".format(user_id)
        )

