import pytest
from model_manager import create_app

app = create_app()

@pytest.fixture()
def app():

    app.config.update({
        "TESTING": True,
    })
    yield app



@pytest.fixture()
def client(app):
    return app.test_client()

def test_request_upload(client):
    response = client.get('/')


