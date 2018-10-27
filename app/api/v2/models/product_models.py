import datetime
import psycopg2
from .database_models import DatabaseConnection
from dbConfig import config


class ProductModel(DatabaseConnection):
    """This class defines models for the products views"""

    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.prod_id = None
        self.quantity = None
        self.date = datetime.datetime.now()
        db = DatabaseConnection()
        db.create_db_tables()

    def create_product(self):
        """Creates a product and adds it to the products table"""
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO products(prod_name, prod_category, prod_price, prod_quantity,"
                       "minimum_allowed,prod_description) "
                       "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                       (self.data["prod_name"],
                        self.data["prod_category"],
                        self.data["prod_price"],
                        self.data["prod_quantity"],
                        self.data["minimum_allowed"],
                        self.data["prod_description"]
                        )
                       )
        cursor.execute("SELECT prod_id FROM products WHERE prod_name = %s",
                       (self.data["prod_name"],))
        row_result = cursor.fetchone()
        self.prod_id = row_result[0]
        self.conn.commit()
        self.conn.close()

    def update_product(self, prod_id):
        """Updates a product in the products table"""
        db = DatabaseConnection()
        self.prod_id = prod_id
        db.create_db_tables()
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE products SET prod_name = %s, prod_category = %s, 
            prod_price = %s, prod_quantity = %s, minimum_allowed = %s, prod_description = %s
            WHERE prod_id = %s""",
            (self.data["prod_name"],
             self.data["prod_category"],
             self.data["prod_price"],
             self.data["prod_quantity"],
             self.data["minimum_allowed"],
             self.data["prod_description"],
             self.prod_id),
        )
        self.conn.commit()
        self.conn.close()

    def get_all_products(self):
        """Fetches all products from the products table"""
        db = DatabaseConnection()
        db.create_db_tables()
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        sql_cmd = "SELECT * FROM products"
        cursor.execute(sql_cmd)
        products = cursor.fetchall()
        all_products = []
        for product in products:
            prod_list = list(product)
            single_product = {"prod_id": prod_list[0],
                              "prod_name": prod_list[1],
                              "prod_category": prod_list[2],
                              "prod_price": prod_list[3],
                              "prod_quantity": prod_list[4],
                              "minimum_allowed": prod_list[5],
                              "prod_description": prod_list[6]
                              }
            prod_list.append(single_product)
        self.conn.commit()
        return all_products

    def get_product_by_id(self, prod_id):
        """Fetches a particular product from the table using the product id of that product"""
        db = DatabaseConnection()
        self.prod_id = prod_id
        db.create_db_tables()
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        cursor.execute(
            "Select * from products where prod_id = %s",
            (self.prod_id,)
        )
        product = cursor.fetchone()
        prod_list = list(product)
        single_product = {"prod_id": prod_list[0],
                          "prod_name": prod_list[1],
                          "prod_category": prod_list[2],
                          "prod_price": prod_list[3],
                          "prod_quantity": prod_list[4],
                          "minimum_allowed": prod_list[5],
                          "prod_description": prod_list[6]
                          }
        prod_list.append(single_product)
        self.conn.commit()
        return prod_list

    def delete_product(self, prod_id):
        self.prod_id = prod_id
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE from products where prod_id = %s",
            (self.prod_id,)
        )
        self.conn.commit()
        self.conn.close()

    def update_prod_quantity(self, quantity, prod_id):
        """Updates a product's quantity after a sale is made"""
        db = DatabaseConnection()
        db.create_db_tables()
        self.quantity = quantity
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE products SET quantity = %s Where prod_id = %s""", (self.quantity, prod_id,)
        )
        self.conn.commit()
        self.conn.close()
