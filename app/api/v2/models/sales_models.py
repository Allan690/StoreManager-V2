import psycopg2
from .database_models import DatabaseConnection
from dbConfig import config


class SalesModel(DatabaseConnection):
    """This class defines methods for the sales views"""

    def __init__(self, user_id=None, product=None, quantity=None):
        super().__init__()
        if product and user_id and quantity:
            self.user_id = user_id
            self.prod_id = product["prod_id"]
            self.quantity = quantity
        db = DatabaseConnection()
        db.create_db_tables()

    def create_sale_record(self):
        """Creates a sale record in the sales table"""
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sales(user_id, product_id, sales_quantity) VALUES(%s,%s,%s)",
            (self.user_id, self.prod_id, self.quantity), )
        self.conn.commit()
        self.conn.close()

    def get_all_sales(self):
        """Fetches all sales from the sales table"""
        db = DatabaseConnection()
        db.create_db_tables()
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        db_sales = "SELECT * FROM sales"
        cursor.execute(db_sales)
        sales = cursor.fetchall()
        all_sales = []
        for sale in sales:
            list_of_sales = list(sale)
            single_sale = {"sales_id": list_of_sales[0],
                           "user_id": list_of_sales[1],
                           "product_id": list_of_sales[2],
                           "sales_quantity": list_of_sales[3]}
            all_sales.append(single_sale)
        self.conn.commit()
        return all_sales

    def get_sale_by_id(self, sale_id):
        """Gets a particular sale from the database using supplied sale id"""
        db = DatabaseConnection()
        self.prod_id = sale_id
        db.create_db_tables()
        params = config()
        self.conn = psycopg2.connect(**params)
        cursor = self.conn.cursor()
        cursor.execute(
            "Select * from sales where prod_id = %s",
            (self.prod_id,)
        )
        sale = cursor.fetchone()
        sale_list = list(sale)
        single_sale = {"sales_id": sale_list[0],
                       "user_id": sale_list[1],
                       "prod_id": sale_list[2],
                       "sales_quantity": sale_list[3]
                       }
        sale_list.append(single_sale)
        self.conn.commit()
        return sale_list
