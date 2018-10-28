from app import flask_app

# update the configurations of our application
flask_app.config.update(
    DEBUG=True
)
flask_app.secret_key = 'hello-there-its-allan'
if __name__ == '__main__':
    flask_app.run()