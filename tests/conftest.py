from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from model_manager import create_app


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
