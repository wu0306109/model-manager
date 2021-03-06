import os
from typing import Any, Mapping

import firebase_admin
from firebase_admin import credentials
from flask import Flask

from .file_manager import FileManager

# process_manager = ProcessManager()


def create_app(test_config: Mapping[str, Any] = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'Hello, World!'

    # register blueprints below
    from . import api
    app.register_blueprint(api.bp)

    return app


cred = credentials.Certificate(
    'secrets/model-manager-349101-firebase-adminsdk-pzrld-ca1a04e3a6.json')
firebase_admin.initialize_app(cred)
file_manager = FileManager()
