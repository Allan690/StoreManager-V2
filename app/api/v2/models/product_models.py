from .database_models import DatabaseConnection


class ProductModel(DatabaseConnection):
    """This class defines models for the products views"""

    def __init__(self, data=None):
        db = DatabaseConnection()
        super().__init__()
        self.data = data
        self.prod_id = None
        self.quantity = None
        self.cursor = db.cursor_obj()

    def create_product(self):
        """Creates a product and adds it to the products table"""
        if self.cursor:
            self.cursor.execute("INSERT INTO products(prod_name, "
                                "prod_category, prod_price, prod_quantity,"
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

    def update_product(self, prod_id):
        """Updates a product in the products table"""
        if self.cursor:
            self.prod_id = prod_id
            self.cursor.execute(
                """UPDATE products SET prod_name = %s,
                 prod_category = %s, 
                prod_price = %s, prod_quantity = %s, 
                minimum_allowed = %s, prod_description = %s
                WHERE prod_id = %s""",
                (self.data["prod_name"],
                 self.data["prod_category"],
                 self.data["prod_price"],
                 self.data["prod_quantity"],
                 self.data["minimum_allowed"],
                 self.data["prod_description"],
                 self.prod_id),
            )
        else:
            return 'error updating the product'

    def update_prod_name(self, prod_id):
        """Updates the name of a product"""
        if self.cursor:
            self.cursor.execute("""UPDATE products SET 
        prod_name = %s where prod_id = %s""",
                                (self.data["prod_name"], prod_id), )

    def update_prod_category(self, prod_id):
        """Updates the category of a product"""
        if self.cursor:
            self.cursor.execute("""UPDATE products SET 
        prod_category = %s where prod_id = %s""",
                                (self.data["prod_category"], prod_id), )

    def update_prod_quantity(self, quantity, prod_id):
        """Updates a product's quantity after a sale is made"""
        self.quantity = quantity
        self.prod_id = prod_id
        self.cursor.execute(
            """UPDATE products SET prod_quantity =%s where 
            prod_id = %s""", (self.quantity, self.prod_id,)
        )

    def update_prod_price(self, prod_id):
        """Updates price of product"""
        if self.cursor:
            self.cursor.execute("""UPDATE products SET
             prod_price = %s where prod_id = %s""",
                                (self.data["prod_price"], prod_id), )

    def update_quantity(self, prod_id):
        if self.cursor:
            self.cursor.execute("""UPDATE products SET
             prod_quantity = %s where prod_id = %s""",
                                (self.data["prod_price"], prod_id), )

    def update_min_allowed(self, prod_id):
        """Updates minimum allowed quantity in inventory"""
        if self.cursor:
            self.cursor.execute("""UPDATE products SET
             minimum_allowed = %s where prod_id = %s""",
                                (self.data["minimum_allowed"], prod_id), )

    def update_prod_description(self, prod_id):
        """Updates the description of the product"""
        if self.cursor:
            self.cursor.execute("""UPDATE products SET 
            prod_description = %s where prod_id = %s""",
                                (self.data["prod_description"], prod_id), )

    def get_all_products(self):
        """Fetches all products from the products table"""
        if self.cursor:
            sql_cmd = "SELECT * FROM products"
            self.cursor.execute(sql_cmd)
            products = self.cursor.fetchall()
            return products

    def get_product_by_id(self, prod_id):
        """Fetches a particular product from the table using the product id of that product"""
        if self.cursor:
            self.prod_id = prod_id
            self.cursor.execute(
                "Select * from products where prod_id = %s",
                (self.prod_id,)
            )
            product = self.cursor.fetchone()
            return product

    def delete_product(self, prod_id):
        if self.cursor:
            self.prod_id = prod_id
            self.cursor.execute(
                "DELETE from products where prod_id = %s",
                (self.prod_id,)
            )
