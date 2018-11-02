import psycopg2
from dbConfig import config, test_config
from sys import modules


class DatabaseConnection(object):
    def __init__(self):
        self.conn = None
        self.cur = None

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
        try:
            if 'pytest' in modules or 'nosetests' in modules:
                params = test_config()
                self.conn = psycopg2.connect(**params)
                self.cur = self.conn.cursor()
                for command in tbl_commands:
                    self.cur.execute(command)
                self.conn.commit()
            else:
                params = config()
                self.conn = psycopg2.connect(**params)
                self.cur = self.conn.cursor()
                for command in tbl_commands:
                    self.cur.execute(command)
                self.conn.commit()

        except Exception as e:
            print(e)
            return "error connecting to the database because {e}"

    def destroy_tables(self):
        """Destroys the database objects"""
        drop_commands = [
            " DROP TABLE IF EXISTS users CASCADE",
            " DROP TABLE IF EXISTS products CASCADE",
            " DROP TABLE IF EXISTS sales CASCADE"
        ]
        for command in drop_commands:
            if 'pytest' in modules or 'nosetests' in modules:
                params = test_config()
                self.conn = psycopg2.connect(**params)
                self.cur = self.conn.cursor()
                self.cur.execute(command)
                self.conn.commit()
            else:
                params = config()
                self.conn = psycopg2.connect(**params)
                self.cur = self.conn.cursor()
                self.cur.execute(command)
                self.conn.commit()


