import firebase_admin
import pytest
from firebase_admin import credentials


@pytest.fixture(scope='function', autouse=True)
def initailize_flask_app() -> None:
    cert = 'secrets/model-manager-349101-firebase-adminsdk-pzrld-ca1a04e3a6.json'
    cred = credentials.Certificate(cert)
    app = firebase_admin.initialize_app(cred)

    yield None

    firebase_admin.delete_app(app)
