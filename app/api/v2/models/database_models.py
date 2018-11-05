import psycopg2
from psycopg2 import extras
from dbConfig import config, test_config
from sys import modules


class DatabaseConnection(object):
    def __init__(self):
        self.conn = None
        self.cur = None
        self.db = None

    def create_db_tables(self):
        """Creates the database tables for users, products and sales"""
        tbl_commands = (
            """CREATE TABLE IF NOT EXISTS users(
                user_id serial PRIMARY KEY,
                email varchar(100) UNIQUE NOT NULL,
                password varchar(100) NOT NULL,
                role varchar(13) NOT NULL
                )
            """,

            """CREATE TABLE IF NOT EXISTS products(
                 prod_id serial PRIMARY KEY,
                 prod_name varchar(250) NOT NULL,
                 prod_category varchar NOT NULL,
                 prod_price int NOT NULL,
                 prod_quantity int NOT NULL,
                 minimum_allowed varchar(255) NOT NULL,
                 prod_description varchar(255) NOT NULL
                 )

                  """,

            """
            CREATE TABLE IF NOT EXISTS sales(
                sales_id serial PRIMARY KEY,
                user_id int REFERENCES users(user_id) NOT NULL,
                product_id int REFERENCES products(prod_id),
                sales_quantity int NOT NULL,
                prod_price int NOT NULL
                )
            """
        )
        for command in tbl_commands:
            cursor = self.cursor_obj()
            if cursor:
                cursor.execute(command)
            else:
                return 'error connecting to the database'

    @staticmethod
    def __connection():
        """Creates a connection to the database"""
        if 'pytest' in modules or 'nosetests' in modules:
            params = test_config()
        else:
            params = config()
        return psycopg2.connect(
            **params
        )

    def get_connection(self):
        """Gets the connection parameters specified above"""
        self.db = DatabaseConnection()
        self.conn = self.db.__connection()
        self.conn.autocommit = True
        return self.conn

    def cursor_obj(self):
        """Defines the cursor"""
        self.db = DatabaseConnection()
        self.cur = self.db.get_connection().cursor(cursor_factory=extras.RealDictCursor)
        return self.cur

    def destroy_tables(self):
        """Destroys the database objects"""
        drop_commands = [
            " DROP TABLE IF EXISTS users CASCADE",
            " DROP TABLE IF EXISTS products CASCADE",
            " DROP TABLE IF EXISTS sales CASCADE"
        ]
        for command in drop_commands:
            cursor = self.cursor_obj()
            if cursor:
                cursor.execute(command)
            else:
                return 'error connecting to the database'

