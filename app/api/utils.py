import re
from flask import jsonify
from app.api.v2.models.user_models import UserModel
from app.api.v2.models.product_models import ProductModel
user_object = UserModel()
prod_obj = ProductModel()


class KeyValidators(object):
    def __init__(self, data):
        self.data = data

    def check_missing_keys_in_product(self):
        if 'prod_name' not in self.data:
            return jsonify({"Message": "Product Name is required!"}), 400
        if 'prod_quantity' not in self.data:
            return jsonify({"Message": "Quantity is required!"}), 400
        if 'prod_price' not in self.data:
            return jsonify({"Message": "Product price required!"}), 400
        if 'prod_category' not in self.data:
            return jsonify({"Message": "Product category is required"}), 400
        if 'minimum_allowed' not in self.data:
            return jsonify(
                {"Message": "Minimum allowed quantity required!"}), 400

    def check_missing_keys_in_login(self):
        if 'email' not in self.data:
            return jsonify({"Message": "Email is required!"}), 400
        if 'password' not in self.data:
            return jsonify({"Message": "Password is required!"}), 400

    def check_missing_keys_in_sales(self):
        if 'prod_id' not in self.data:
            return jsonify({"Message": "Product ID is required!"}), 400
        if 'quantity' not in self.data:
            return jsonify({"Message": "Product quantity is required!"}), 400


# noinspection PyMethodParameters
class Validator(object):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def validate_user(data):
        validate_email = Validator.validate_email(data['email'])
        if data['email'] == "" or data['password'] == "":
            return jsonify(
                {'Message': "Both email and password are required"}), 400
        for x in data['password']:
            if x.isspace():
                return jsonify(
                    {"Message": "Password can't contain spaces"}), 400
        if len(data['password'].strip()) < 8:
            return jsonify(
                {"Message": "Password should have at least 8 characters"}), 400
        if validate_email:
            return jsonify(
                {"Message": "Wrong email format: Enter a valid email address"}
            ), 400
        users = user_object.get_all_users()
        for user in users:
            if data["email"] == user["email"]:
                return jsonify({'Message': "User already exists"}), 400

    def validate_product(data):
        if not data or not data['prod_name']:
            return jsonify({"Message": "Name is required!"}), 400
        elif not data['prod_quantity'] or data['prod_quantity'] == 0:
            return jsonify({"Message": "Quantity is required!"}), 400
        elif not data['prod_description']:
            return jsonify({"Message": "Description is required!"}), 400
        if not isinstance(data['prod_description'], str):
            return jsonify({"Message": "Description must be a string!"}), 400
        if not isinstance(data['prod_name'], str):
            return jsonify({"Message": "Product name must be a string!"}), 400

        elif not data['prod_price'] or data['prod_price'] == 0:
            return jsonify({"Message": "Price is required!"}), 400

        if not isinstance(data['prod_quantity'], int):
            return jsonify({"Message": "Quantity must be a number!"}), 400
        if not isinstance(data['prod_price'], int):
            return jsonify({"Message": "Price must be a number!"}), 400

        if not data['prod_category'] or data['prod_category'] == "":
            return jsonify({"Message": "Product category required"}), 400
        if not isinstance(data['prod_category'], str):
            return jsonify(
                {"Message": "Product category must be a string!"}), 400

        if not isinstance(data['minimum_allowed'], int):
            return jsonify(
                {"Message": "Minimum allowed quantity must be a number!"}), 400
        if not data['minimum_allowed'] or data['minimum_allowed'] == 0:
            return jsonify(
                {"Message": "Minimum allowed quantity required!"}), 400
        products = prod_obj.get_all_products()
        for product in products:
            if data["prod_name"] == product["prod_name"]:
                return jsonify({'Message': "Product already exists"}), 400
            prod_name_db = str(data["prod_name"])
            prod_name_supplied = str(product["prod_name"])
            if prod_name_db.lower() == prod_name_supplied:
                return jsonify({'Message': "Product already exists"}), 400

    def validate_update(data):
        if data["prod_name"]:
            if not isinstance(data['prod_name'], str):
                return jsonify(
                    {"Message": "Product name must be a string!"}), 400
        if data["prod_quantity"]:
            if not isinstance(data['prod_quantity'], int):
                return jsonify({"Message": "Quantity must be a number!"}), 400
        if data["prod_description"]:
            if not isinstance(data['prod_description'], str):
                return jsonify(
                    {"Message": "Description must be a string!"}), 400
            if not data['prod_description']:
                return jsonify({"Message": "Description is required!"}), 400
        if data["prod_price"]:
            if not isinstance(data['prod_price'], int):
                return jsonify({"Message": "Price must be a number!"}), 400
            elif not data['prod_price'] or data['prod_price'] == 0:
                return jsonify({"Message": "Price is required!"}), 400
        if data["minimum_allowed"]:
            if not isinstance(data['minimum_allowed'], int):
                return jsonify(
                    {"Message": "Minimum allowed quantity must be a number!"}
                ), 400
            if not data['minimum_allowed'] or data['minimum_allowed'] == 0:
                return jsonify(
                    {"Message": "Minimum allowed quantity required!"}), 400

    def validate_sales(data):
        if not data or not data['prod_id']:
            return jsonify({"Message": "Product ID is required!"}), 400
        if not isinstance(data['prod_id'], int):
            return jsonify({"Message": "Product ID must be a number!"}), 400
        elif not data['quantity'] or data['quantity'] == 0:
            return jsonify({"Message": "Quantity is required!"}), 400
        if not isinstance(data['quantity'], int):
            return jsonify({"Message": "Quantity must be a number!"}), 400
        if data['prod_id'] == 0:
            return jsonify({"Message": "Product ID cannot be 0!"}), 400

    def validate_login(auth):

        if not auth:
            return jsonify({"Message": "Email and password required!"}), 401
        if not auth['email']:
            return jsonify({"Message": "Email is required"}), 401
        if not auth['password']:
            return jsonify({"Message": "password is required"}), 401
        if not isinstance(auth['password'], str):
            return jsonify({"Message": "Password must be a string!"}), 400
        if not isinstance(auth['email'], str):
            return jsonify({"Message": "Email must be a string!"}), 400
        validate_em = Validator.validate_email(auth["email"])
        if validate_em:
            return jsonify({"Message":
                            "Wrong email format: Enter a valid email address"}
                           ), 400

    def validate_make_admin(data):
        if not data:
            return jsonify({"Message": "Email is required"}), 401
        if not isinstance(data["email"], str):
            return jsonify({"Message": "Email must be a string!"}), 400
        validate_email = Validator.validate_email(data['email'])
        if validate_email:
            return jsonify(
                {"Message": "Wrong email format: Enter a valid email address"}
            ), 400

    def validate_email(email):
        """This method uses a regular expression to validate email
        entered by user"""
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                        email):
            return True
        return False




