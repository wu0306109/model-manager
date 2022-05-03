from collections.abc import Generator

import firebase_admin
import pytest
from firebase_admin import credentials
from flask import Flask
from flask.testing import FlaskClient
from model_manager import create_app


@pytest.fixture(scope='function', autouse=True)
def initailize_flask_app() -> None:
    cred = credentials.Certificate(
        'secrets/model-manager-349101-firebase-adminsdk-pzrld-ca1a04e3a6.json')
    app = firebase_admin.initialize_app(cred)

    yield None

    firebase_admin.delete_app(app)


@pytest.fixture()
def app() -> Generator[Flask]:
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app) -> FlaskClient:
    return app.test_client()
