"""Controller file that registers the blueprints of our application and creates
the flask application"""
from flask import Flask
from .api.v2.views.product_views import prod as product_bp
from .api.v2.views.users_views import user_dec as user_bp
# create our flask application
flask_app = Flask(__name__)
# register the blueprints of our models
flask_app.secret_key = 'hello-there-its-allan'
flask_app.register_blueprint(product_bp)
flask_app.register_blueprint(user_bp)
