from flask import Flask
from flask_cors import CORS
from module.auth import auth
from module.messaging import messaging


def create_app():
    app = Flask(__name__)
    CORS(
        app,
        origins=["http://localhost:5173", "http://skpy.adityakhot.com","https://skpy.adityakhot.com"]
    )
    app.config.from_pyfile("config.py")
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    register_blueprints(app)

    return app


def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(messaging)


if __name__ == "__main__":
    create_app().run(debug=False)
