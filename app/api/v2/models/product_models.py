import psycopg2
import psycopg2.extras
from .database_models import DatabaseConnection
from dbConfig import config


class ProductModel(DatabaseConnection):
    """This class defines models for the products views"""

    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.prod_id = None
        self.quantity = None
        db = DatabaseConnection()
        db.create_db_tables()
        params = config()
        self.conn = psycopg2.connect(**params)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def create_product(self):
        """Creates a product and adds it to the products table"""
        self.cursor.execute("INSERT INTO products(prod_name, prod_category, prod_price, prod_quantity,"
                            "minimum_allowed,prod_description) "
                            "VALUES(%s,%s,%s,%s,%s,%s)",
                            (self.data["prod_name"],
                             self.data["prod_category"],
                             self.data["prod_price"],
                             self.data["prod_quantity"],
                             self.data["minimum_allowed"],
                             self.data["prod_description"],
                             )
                            )
        self.conn.commit()
        self.conn.close()

    def update_product(self, prod_id):
        """Updates a product in the products table"""
        self.prod_id = prod_id
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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

    def update_prod_name(self, prod_id):
        """Updates the name of a product """
        self.cursor.execute("""UPDATE products SET prod_name = %s where prod_id = %s""",
                            (self.data["prod_name"], prod_id),)
        self.conn.commit()

    def update_prod_category(self, prod_id):
        """Updates the category of a product"""
        self.cursor.execute("""UPDATE products SET prod_category = %s where prod_id = %s""",
                            (self.data["prod_category"], prod_id),)
        self.conn.commit()

    def update_prod_quantity(self, quantity, prod_id):
        """Updates a product's quantity after a sale is made"""
        self.quantity = quantity
        self.prod_id = prod_id
        self.cursor.execute(
            """UPDATE products SET prod_quantity =%s where prod_id = %s""", (self.quantity, self.prod_id,)
        )
        self.conn.commit()

    def update_prod_price(self, prod_id):
        """Updates price of product"""
        self.cursor.execute("""UPDATE products SET prod_price = %s where prod_id = %s""",
                            (self.data["prod_price"], prod_id),)
        self.conn.commit()

    def update_quantity(self, prod_id):
        self.cursor.execute("""UPDATE products SET prod_quantity = %s where prod_id = %s""",
                                (self.data["prod_price"], prod_id), )
        self.conn.commit()

    def update_min_allowed(self, prod_id):
        """Updates minimum allowed quantity in inventory"""
        self.cursor.execute("""UPDATE products SET minimum_allowed = %s where prod_id = %s""",
                            (self.data["minimum_allowed"], prod_id), )
        self.conn.commit()

    def update_prod_description(self, prod_id):
        """Updates the description of the product"""
        self.cursor.execute("""UPDATE products SET prod_description = %s where prod_id = %s""",
                            (self.data["prod_description"], prod_id), )
        self.conn.commit()

    def get_all_products(self):
        """Fetches all products from the products table"""
        sql_cmd = "SELECT * FROM products"
        self.cursor.execute(sql_cmd)
        products = self.cursor.fetchall()
        self.conn.commit()
        all_products = []
        for prod in products:
            prod_dict = {
                "prod_id": prod[0],
                "prod_name": prod[1],
                "prod_category": prod[2],
                "prod_price": prod[3],
                "prod_quantity": prod[4],
                "minimum_allowed": prod[5],
                "prod_description": prod[6]
            }
            all_products.append(prod_dict)
        return all_products

    def get_product_by_id(self, prod_id):
        """Fetches a particular product from the table using the product id of that product"""
        self.prod_id = prod_id
        self.cursor.execute(
            "Select * from products where prod_id = %s",
            (self.prod_id,)
        )
        product = self.cursor.fetchone()
        self.conn.commit()
        if product:
            prod = []
            prod_dict = {
                "prod_id": product[0],
                "prod_name": product[1],
                "prod_category": product[2],
                "prod_price": product[3],
                "prod_quantity": product[4],
                "minimum_allowed": product[5],
                "prod_description": product[6]
            }
            prod.append(prod_dict)
            return prod
        return 'Product does not exist'

    def delete_product(self, prod_id):
        self.prod_id = prod_id
        self.cursor.execute(
            "DELETE from products where prod_id = %s",
            (self.prod_id,)
        )
        self.conn.commit()
        self.conn.close()
