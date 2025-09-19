def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_register_page(client):
    response = client.get('/registro')
    assert response.status_code == 200
