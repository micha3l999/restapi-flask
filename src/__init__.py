from flask import Flask
from flask_jwt_extended import JWTManager
from .services.authentication.auth import auth
from .services.bookmarks.bookmarks import bookmarks
from .models.instance import db
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if not test_config:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    jwt = JWTManager()
    jwt.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app
