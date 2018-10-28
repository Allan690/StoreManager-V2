import re
from flask import jsonify, abort
from app.api.v2.models.user_models import UserModel
from app.api.v2.models.product_models import ProductModel
user_object = UserModel()
prod_obj = ProductModel()


# noinspection PyMethodParameters
class Validator(object):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def validate_user(data):
        validate_email = Validator.validate_email(data['email'])
        if data['email'] == "" or data['password'] == "":
            return jsonify({'Message': "Both email and password are required"}), 400
        for x in data['password']:
            if x.isspace():
                return jsonify({"Message": "Password can't contain spaces"}), 400
        if len(data['password'].strip()) < 8:
            return jsonify({"Message": "Password should have at least 8 characters"}), 400
        if len(data['role'].strip()) < 5:
            return jsonify({"Message": "Role should have at least 5 characters"}), 400
        for x in data['role']:
            if x.isspace():
                return jsonify({"Message": "Role can't contain spaces"}), 400
        if validate_email:
            return jsonify({"Message": "Wrong email format: Enter a valid email address"}), 400
        users = user_object.get_all_users()
        for user in users:
            if data["email"] == user["email"]:
                return jsonify({'Message': "User already exists"}), 400

    def validate_product(data):
        if not data or not data['name']:
            return jsonify({"Message": "Name is required!"}), 400
        elif not data['quantity'] or data['quantity'] == 0:
            return jsonify({"Message": "Quantity is required!"}), 400
        elif not data['description']:
            return jsonify({"Message": "Description is required!"}), 400
        if not isinstance(data['description'], str):
            return jsonify({"Message": "Description must be a string!"}), 400
        if not isinstance(data['name'], str):
            return jsonify({"Message": "Product name must be a string!"}), 400
        elif not data['price'] or data['price'] == 0:
            return jsonify({"Message": "Price is required!"}), 400
        if not isinstance(data['quantity'], int):
            return jsonify({"Message": "Quantity must be a number!"}), 400
        if not isinstance(data['price'], int):
            return jsonify({"Message": "Price must be a number!"}), 400
        products = prod_obj.get_all_products()
        for product in products:
            if data["prod_id"] == product["prod_id"]:
                return jsonify({'Message': "Product already exists"}), 400

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

    def validate_email(email):
        """This method uses a regular expression to validate email entered by user"""
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return True
        return False



