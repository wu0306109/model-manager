from collections.abc import Generator
from datetime import datetime

import pytest
from flask import Flask
from model_manager import create_app, file_manager
from model_manager.file_manager import File
from werkzeug.test import Client


@pytest.fixture
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


def test_hello_world(client: Client) -> None:
    response = client.get('/api/')
    assert response.data == b'Hello, World!'


def test_list_files(client: Client) -> None:
    # TODO: add files by uploading API rather than by file manager
    file1 = File(
        name='test-file-1',
        type='dataset',
        description='test-file-1',
        path='./test-file-1.csv',
        uploader='test',
        upload_time=datetime(2022, 5, 3, 12, 43),
        last_used_time=datetime(2022, 5, 3, 12, 44),
    )
    file2 = File(
        name='test-file-2',
        type='dataset',
        description='test-file-2',
        path='./test-file-2.csv',
        uploader='test',
        upload_time=datetime(2022, 5, 3, 11, 43),
        last_used_time=datetime(2022, 5, 3, 11, 44),
    )
    file_manager.add(file1)
    file_manager.add(file2)

    result = client.get('/api/list-files').json
    assert 'test-file-1' in result
    assert result['test-file-1'] == {
        'type': 'dataset',
        'description': 'test-file-1',
        'path': './test-file-1.csv',
        'uploader': 'test',
        'upload_time': 1651552980.0,
        'last_used_time': 1651553040.0,
    }
    assert 'test-file-2' in result
    assert result['test-file-2'] == {
        'type': 'dataset',
        'description': 'test-file-2',
        'path': './test-file-2.csv',
        'uploader': 'test',
        'upload_time': 1651549380.0,
        'last_used_time': 1651549440.0,
    }
