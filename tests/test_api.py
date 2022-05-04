import os
from collections.abc import Generator
from datetime import datetime

import pandas as pd
import pytest
from flask import Flask
from model_manager import create_app, file_manager
from model_manager.file_manager import File
from werkzeug.test import Client


@pytest.fixture()
def app():
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
    assert 'test-file-1' in result['result']
    assert 'test-file-2' in result['result']


def test_view_file_detail(client: Client) -> None:
    dataframe = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6],
        'c': [7, 8, 9],
    })
    dataframe.to_csv('./tests/test-dataframe-2.csv', index=False)
    file = File(
        name='test-csv-file-2',
        type='dataset',
        description='test-csv-file-2',
        path='./tests/test-dataframe-2.csv',
        uploader='test',
        upload_time=datetime(2022, 5, 3, 11, 43),
        last_used_time=datetime(2022, 5, 3, 11, 44),
    )
    file_manager.add(file)

    result = client.get('/api/files/test-csv-file-2/detail').json
    assert result == {
        file.name: {
            'type': file.type,
            'description': file.description,
            'path': file.path,
            'uploader': file.uploader,
            'upload_time': file.upload_time.timestamp(),
            'last_used_time': file.last_used_time.timestamp(),
        },
    }

    # TODO: make execute even when exceptions issueed before
    os.remove('./tests/test-dataframe-2.csv')
