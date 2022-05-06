from flask import Flask
from .services.authentication.auth import auth
from .services.bookmarks.bookmarks import bookmarks

import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if not test_config:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
        )
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app
