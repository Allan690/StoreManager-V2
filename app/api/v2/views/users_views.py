from flask import jsonify, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ..models.user_models import UserModel
from ...utils import Validator
user_dec = Blueprint('v1_user', __name__)
user_obj = UserModel()


# noinspection PyMethodParameters
class UserViews(object):
    """This class defines the views of the user"""

    @user_dec.route('/api/v2/auth/signup', methods=['POST'])
    @jwt_required
    def create_attendant_user():
        """This view creates an attendant user"""
        email = get_jwt_identity()
        user = user_obj.get_role_by_email(email)
        role = user["role"]
        if role != "admin":
            return jsonify({"Message": "You must be an admin to perform this action"}), 403
        data = request.get_json()
        validate = Validator(data)
        if validate.validate_user():
            return validate.validate_user()
        password_hash = generate_password_hash(data['password'], method='sha256')
        email = data["email"]
        role = data["role"]
        user = UserModel(email, password_hash, role)
        user.create_attendant_user()
        return jsonify({"Message": "Attendant user registered successfully"}), 201

    @user_dec.route('/api/v2/auth/signup-admin', methods=['POST'])
    def create_admin_user():
        """This view creates an admin user"""
        data = request.get_json()
        validate = Validator(data)
        if validate.validate_user():
            return validate.validate_user()
        password_hash = generate_password_hash(data['password'], method='sha256')
        email = data["email"]
        role = data["role"]
        user = UserModel(email, password_hash, role)
        user.create_admin_user()
        return jsonify({"Message": "Admin user registered successfully"}), 201

    @user_dec.route('/api/v2/auth/make-admin', methods=['PUT'])
    @jwt_required
    def make_admin_user():
        """This view makes an attendant user an admin"""
        email = get_jwt_identity()
        user = user_obj.get_role_by_email(email)
        role = user["role"]
        if role != "admin":
            return jsonify({"Message": "You must be an admin to perform this action"}), 403
        data = request.get_json()
        user_id = data["user_id"]
        ret_users = user_obj.get_user_by_id(user_id)
        print(ret_users)
        if not ret_users:
            return jsonify({"Message": "User not found!"}), 404
        user_obj.make_admin(user_id)
        return jsonify({"Message": "Attendant made admin successfully!"}), 200

    @user_dec.route('/api/v2/auth/users', methods=['GET'])
    @jwt_required
    def get_all_users():
        email = get_jwt_identity()
        user = user_obj.get_role_by_email(email)
        role = user["role"]
        if role != "admin":
            return jsonify({"Message": "You must be an admin to perform this action"}), 403
        users = user_obj.get_all_users()
        return jsonify({"Users": users}), 200

    @user_dec.route('/api/v2/auth/login', methods=['POST'])
    def login_user():
        data = request.get_json()
        validate = Validator(data)
        if validate.validate_login():
            return validate.validate_login()
        users = user_obj.get_all_users()
        for user in users:
            if check_password_hash(user['password'], data['password']):
                access_token = create_access_token(identity=data["email"])
                return jsonify({"token": access_token}), 200
        return jsonify({"Message": "User not found!"}), 404



