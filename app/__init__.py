"""Controller file that registers the blueprints of our application and creates
the flask application"""
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .api.v2.views.product_views import prod as product_bp
from .api.v2.views.users_views import user_dec as user_bp
# create our flask application
flask_app = Flask(__name__)
# register the blueprints of our models
CORS(flask_app)
flask_app.config['JWT_SECRET_KEY'] = 'hello-there-im-allan'
jwt = JWTManager(flask_app)
flask_app.register_blueprint(product_bp)
flask_app.register_blueprint(user_bp)


@flask_app.errorhandler(404)
def handle_404_errors(e):
    return jsonify(
            {"Message": "The page could not be found. Please check the route"}
        ), 404


@flask_app.errorhandler(405)
def handle_405_errors(e):
    return jsonify(
        {"Message": "The method is not allowed for the requested URL. Please check your HTTP method"}
    ), 405


