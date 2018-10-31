from flask import jsonify, request, Blueprint
from ...utils import Validator
from ..models.product_models import ProductModel
from ..models.sales_models import SalesModel
from .users_views import login_token

prod = Blueprint('v2_prods', __name__)
prod_obj = ProductModel()
sales_obj = SalesModel()


# noinspection PyMethodParameters
class ProductViews(object):
    def __init__(self, current_user):
        self.current_user = current_user

    def __getitem__(self, item):
        return self.current_user[item]

    @prod.route('/api/v2/products', methods=['POST'])
    @login_token
    def post_product(current_user):
        if current_user and current_user["role"] != "Admin" or current_user["role"] != "admin":
            return jsonify({"Message": "You must be an admin to add a product"}), 403
        data = request.get_json()
        validate = Validator(data)
        if validate.validate_product():
            return validate.validate_product()
        product = ProductModel(data)
        product.create_product()
        return jsonify({"Message": "Product registered successfully",
                        "Products Profile": prod_obj.get_all_products()}), 201

    @prod.route('/api/v2/products', methods=['GET'])
    @login_token
    def get_all_products(current_user):
        """Fetches all products from the database and returns them"""
        if current_user:
            prods = prod_obj.get_all_products()
            if len(prods) > 0:
                return jsonify({"All products": prods}), 200
            else:
                return jsonify({"Message": "Product list empty!"}), 404
        else:
            return jsonify({"Message": "Please log in to fetch your products"}), 401

    @prod.route('/api/v2/products/<int:product_id>', methods=['GET'])
    @login_token
    def get_products_by_id(current_user, product_id):
        """Fetches a product using supplied product id"""
        product = prod_obj.get_product_by_id(product_id)
        if len(product) == 0:
            return jsonify({"Message": "Product list is empty!"}), 404
        if current_user:
            return jsonify({"Product Profile": product}), 200
        return jsonify({"Message": "Product not found!"}), 404

    @prod.route('/api/v2/products/<int:product_id>', methods=['PUT'])
    @login_token
    def update_products(current_user, product_id):
        """Updates a specific product's details"""
        if current_user and current_user["role"] != "admin":
            return jsonify({"Message": "Only admin can update the product!"}), 403
        data = request.get_json()
        validate = Validator(data)
        if validate.validate_product():
            return validate.validate_product()
        product_obj = ProductModel(data)
        prods = product_obj.get_all_products()
        if len(prods) == 0:
            return jsonify({"Message": "Product list is empty!"}), 404
        resp = product_obj.get_product_by_id(product_id)
        if resp:
            product_obj.update_product(product_id)
            return jsonify({"Message": "Product updated successfully!",
                            "Products": prods}), 200
        return jsonify({"Message": "Product not found!"}), 404

    @prod.route('/api/v2/products/<int:product_id>', methods=['DELETE'])
    @login_token
    def delete_product_by_id(current_user, product_id):
        if current_user["role"] == "admin":
            resp = prod_obj.get_product_by_id(product_id)
            if resp:
                prod_obj.delete_product(product_id)
                return jsonify({"Message": "Product deleted successfully!"}), 200
            return jsonify({"Message": "Product not found!"}), 404
        return jsonify({"Message": "Only admin can delete a product"}), 400

    @prod.route('/api/v2/sales', methods=['POST'])
    @login_token
    def create_sale_record(current_user):
        """Creates a sales record and saves it to the database"""
        data = request.get_json()
        if current_user and current_user["role"] == "attendant":
            validate = Validator(data)
            if validate.validate_sales():
                return validate.validate_sales()
            prod_id = data["prod_id"]
            sold_quantity = data["quantity"]
            user_id = current_user["user_id"]
            resp = prod_obj.get_product_by_id(prod_id)
            if resp["quantity"] > sold_quantity:
                prod_obj.update_prod_quantity(resp["quantity"]-sold_quantity, prod_id)
                SalesModel(user_id, resp, sold_quantity)
                return jsonify({"Message": "Sale record created successfully!"}), 201
            return jsonify({"Message": "Sold quantity exceeds what is in stock!"}), 400
        return jsonify({"Message": "You must be an attendant to make a sale record"}), 401

    @prod.route('/api/v2/sales', methods=['GET'])
    @login_token
    def get_all_sales(current_user):
        """Fetches all sales from the database"""
        if current_user:
            sales = sales_obj.get_all_sales()
            if len(sales) > 0:
                return jsonify({"All Sales": sales}), 200
            else:
                return jsonify({"Message": "Sales list empty!"}), 404
        else:
            return jsonify({"Message": "Please log in to fetch your sales"}), 401

    @prod.route('/api/v2/sales/<int:sales_id>', methods=['GET'])
    @login_token
    def get_sales_by_id(current_user, sales_id):
        """Fetches a sale from the database using supplied id"""
        """Fetches a product using supplied product id"""
        sale = sales_obj.get_sale_by_id(sales_id)
        if len(sale) == 0:
            return jsonify({"Message": "Sales list is empty!"}), 404
        if current_user:
            return jsonify({"Sale Profile": sale}), 200
        return jsonify({"Message": "Sale not found!"}), 404

