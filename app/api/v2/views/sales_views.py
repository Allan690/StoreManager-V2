from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...utils import Validator, KeyValidators
from ..models.product_models import ProductModel
from ..models.sales_models import SalesModel
from ..models.user_models import UserModel

sale = Blueprint('v2_sales', __name__)
prod_obj = ProductModel()
sales_obj = SalesModel()
users_obj = UserModel()


@sale.route('/api/v2/sales', methods=['POST'])
@jwt_required
def create_sale_record():
    """Creates a sales record and saves it to the database"""
    email = get_jwt_identity()
    user = users_obj.get_user_by_email(email)
    role = user["role"]
    if role != "attendant":
        return jsonify({"Message":
                        "You must be an attendant to sale a product"}), 401
    data = request.get_json()
    key_valid = KeyValidators(data)
    if key_valid.check_missing_keys_in_sales():
        return key_valid.check_missing_keys_in_sales()
    validate = Validator(data)
    if validate.validate_sales():
        return validate.validate_sales()
    try:
        user_id = user["user_id"]
        prod_id = data["prod_id"]
        sold_quantity = data["quantity"]
    except KeyError:
        return jsonify({"Message": "You have a missing parameter!"}), 400
    resp = prod_obj.get_product_by_id(prod_id)
    if not resp:
        return jsonify({"Message": "Product was not found!"}), 404
    prod_price = resp['prod_price']
    if resp['prod_quantity'] > sold_quantity \
            and resp['prod_quantity'] > int(resp['minimum_allowed']):
        prod_obj.update_prod_quantity(
            resp["prod_quantity"] - sold_quantity, prod_id)
        sale_obj = SalesModel(user_id, prod_id, sold_quantity, prod_price)
        sale_obj.create_sale_record()
        return jsonify({"Message":
                        "Sale record created successfully!"}), 201
    return jsonify({"Message":
                    "Sold quantity exceeds what is in stock!"}), 400


@sale.route('/api/v2/sales', methods=['GET'])
@jwt_required
def get_all_sales():
    """Fetches all sales from the database"""
    email = get_jwt_identity()
    user = users_obj.get_user_by_email(email)
    role = user["role"]
    user_id = user["user_id"]
    if role != "admin":
        return jsonify({"Message": "Sale records retrieved successfully!",
                        "Sale records":
                            sales_obj.get_sales_by_user_id(user_id)}), 200
    sales = sales_obj.get_all_sales()
    if not sales or len(sales) == 0:
        return jsonify({"Message": "Sales not found!"}), 404
    return jsonify({"Message": "Sales retrieved successfully!",
                    "All Sales": sales
                    }), 200


@sale.route('/api/v2/sales/<int:sales_id>', methods=['GET'])
@jwt_required
def get_sales_by_id(sales_id):
    """Fetches a sale from the database using supplied id"""
    sale_one = sales_obj.get_sale_by_id(sales_id)
    if not sale_one or len(sale_one) == 0:
        return jsonify({"Message": "Sales record not found!"}), 404
    return jsonify({"Message": "Sale retrieved successfully",
                    "Sale Profile": sale_one}), 200
