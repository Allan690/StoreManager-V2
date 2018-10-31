from flask import jsonify, request, Blueprint, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import os
import datetime
from ..models.user_models import UserModel
from ...utils import Validator
os.environ['SECRET'] = 'hello-there-its-allan'
user_dec = Blueprint('v1_user', __name__)
user_obj = UserModel()


def login_token(f):
    """All endpoints that need log in will be wrapped by this decorator"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'Message': 'You need to log in'}), 401
        try:
            data = jwt.decode(token, os.getenv('SECRET'), options={'verify_exp': False})
            users = user_obj.get_all_users()
            for user in users:
                if user["email"] == data["email"]:
                    current_user = user
        except BaseException:
            return jsonify({'Message': 'Invalid request!Token is invalid'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


# noinspection PyMethodParameters
class UserViews(object):
    """This class defines the views of the user"""

    def __init__(self, current_user):
        self.current_user = current_user

    def __getitem__(self, item):
        return self.current_user[item]

    @user_dec.route('/api/v1/auth/signup', methods=['POST'])
    def create_attendant_user():
        """This view creates an attendant user"""
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

    @user_dec.route('/api/v1/auth/signup-admin', methods=['POST'])
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

    @user_dec.route('/api/v1/auth/signup/<int:user_id>', methods=['PUT'])
    @login_token
    def make_admin(current_user, user_id):
        """This view makes an attendant user an admin"""
        if current_user["role"] == "Admin":
            users = user_obj.get_all_users()
            for user in users:
                if user["role"] != "admin":
                    user_obj.make_admin(user_id)
                    return jsonify({"Message": "User updated to admin role"}), 201
                else:
                    return jsonify({"Message": "User is already an admin"}), 403
            return jsonify({"Message": "User does not exist!"}), 404
        return jsonify({"Message": "Denied. Only admin user can make attendant admin"}), 401

    @user_dec.route('/api/v1/auth/users', methods=['GET'])
    @login_token
    def get_all_users(current_user):
        return jsonify({"users": user_obj.get_all_users()}), 200

    @user_dec.route('/api/v1/auth/login', methods=['POST'])
    def login_user():
        data = request.get_json()
        validate = Validator(data)
        if validate.validate_login():
            return validate.validate_login()
        users = user_obj.get_all_users()
        for user in users:
            if check_password_hash(user['password'], data['password']):
                session['loggedin'] = True
                session['email'] = data['email']
                token = jwt.encode(
                    dict(email=user['email'], exp=datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)),
                    os.getenv('SECRET'))
                return jsonify({"token": token.decode('UTF-8')}), 200
        return jsonify({"Message": "login invalid!"}), 401
