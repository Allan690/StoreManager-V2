import psycopg2
import psycopg2.extras
from .database_models import DatabaseConnection
from dbConfig import config


class SalesModel(DatabaseConnection):
    """This class defines methods for the sales views"""

    def __init__(self, user_id=None, prod_id=None, quantity=None, price=None):
        super().__init__()
        if prod_id and user_id and quantity and price:
            self.user_id = user_id
            self.prod_id = prod_id
            self.quantity = quantity
            self.price = price
        db = DatabaseConnection()
        db.create_db_tables()
        params = config()
        self.conn = psycopg2.connect(**params)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def create_sale_record(self):
        """Creates a sale record in the sales table"""

        self.cursor.execute(
            "INSERT INTO sales(user_id, product_id, sales_quantity, prod_price) VALUES(%s,%s,%s,%s)",
            (self.user_id, self.prod_id, self.quantity, self.price), )
        self.conn.commit()
        self.conn.close()

    def get_all_sales(self):
        """Fetches all sales from the sales table"""
        db_sales = "SELECT * FROM sales"
        self.cursor.execute(db_sales)
        sales = self.cursor.fetchall()
        sales_list = []
        for sale in sales:
            sales_dict = {
                "sales_id": sale[0],
                "user_id": sale[1],
                "prod_id": sale[2],
                "sales_quantity": sale[3],
                "sale_price": sale[4]
            }
            sales_list.append(sales_dict)
        self.conn.commit()
        return sales_list

    def get_sale_by_id(self, sale_id):
        """Gets a particular sale from the database using supplied sale id"""
        self.prod_id = sale_id
        self.cursor.execute(
            "Select * from sales where prod_id = %s",
            (self.prod_id,)
        )
        sale = self.cursor.fetchone()
        sales_dict = {
            "sales_id": sale[0],
            "user_id": sale[1],
            "prod_id": sale[2],
            "sales_quantity": sale[3],
            "sales_price": sale[4]
        }
        self.conn.commit()
        return sales_dict
