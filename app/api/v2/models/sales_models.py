from .database_models import DatabaseConnection
from .user_models import UserModel
db = DatabaseConnection()
user = UserModel()


class SalesModel(DatabaseConnection):
    """This class defines methods for the sales views"""

    def __init__(self, user_id=None, prod_id=None, quantity=None, price=None):
        super().__init__()
        self.cursor = db.cursor_obj()
        if prod_id and user_id and quantity and price:
            self.user_id = user_id
            self.prod_id = prod_id
            self.quantity = quantity
            self.price = price

    def create_sale_record(self):
        """Creates a sale record in the sales table"""
        self.cursor.execute(
            "INSERT INTO sales(user_id, product_id, sales_quantity, prod_price)"
            " VALUES(%s,%s,%s,%s)",
            (self.user_id, self.prod_id, self.quantity, self.price), )

    def get_all_sales(self):
        """Fetches all individual attendant sales from the sales table"""
        self.cursor.execute("Select * from sales")
        sales = self.cursor.fetchall()
        return sales

    def get_sales_by_user_id(self, user_id):
        """Fetches a sale using user_id """
        self.cursor.execute(
            "Select * from sales where user_id = %s",
            (user_id,)
        )
        sale = self.cursor.fetchall()
        return sale

    def get_sale_by_id(self, sale_id):
        """Gets a particular sale from the database using supplied sale id"""
        self.prod_id = sale_id
        self.cursor.execute(
            "Select * from sales where sales_id = %s",
            (self.prod_id,)
        )
        sale = self.cursor.fetchone()
        return sale


