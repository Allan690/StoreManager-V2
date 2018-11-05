"""Controller file that registers the blueprints of our application and creates
the flask application"""
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from .api.v2.views.product_views import prod as product_bp
from .api.v2.views.users_views import user_dec as user_bp
# create our flask application
flask_app = Flask(__name__)
# register the blueprints of our models
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


@flask_app.errorhandler(500)
def handle_500_errors(e):
    return jsonify(
        {"Message": "There was an internal server error."}
    ), 500


@flask_app.route('/')
def index_route():
    """Defines the index route"""
    return "<p>Find the app documentation <a href='https://apimatic.io/apidocs/storemanager-api-v2/'>here</a></p>"
