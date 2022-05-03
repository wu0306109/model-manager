from collections.abc import Generator

import pytest
from flask import Flask
from model_manager import create_app
from werkzeug.test import Client


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
def client(app) -> Client:
    return app.test_client()


def test_hello_world(client) -> None:
    response = client.get('/api/')
    assert response.data == b'Hello, World!'
