def test_hello_world(client) -> None:
    response = client.get('/api/')
    assert response.data == b'Hello, World!'
