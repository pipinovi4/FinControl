# tests/routes/test_auth/test_broker_auth.py

def test_login_broker_web(client):
    """
    Test if login works for broker role on web with valid credentials.
    """
    response = client.post("/api/auth/login/broker/web", data={"username": "broker", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_broker_web(client):
    """
    Test if register works for broker role on web.
    """
    response = client.post("/api/auth/register/broker/web", data={"username": "new_broker", "password": "password"})
    assert response.status_code == 201
    assert "username" in response.json()

def test_login_broker_bot(client):
    """
    Test if login fails for broker role on bot.
    """
    response = client.post("/api/auth/login/broker/bot", data={"username": "broker", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for broker login on bot

def test_register_broker_bot(client):
    """
    Test if registration fails for broker role on bot.
    """
    response = client.post("/api/auth/register/broker/bot", data={"username": "new_broker_bot", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for broker registration on bot

def test_login_broker_invalid_route(client):
    """
    Test if login fails for broker role when trying to log in on a non-existent route.
    """
    response = client.post("/api/auth/login/invalid/broker", data={"username": "broker", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for invalid route

# tests/routes/test_auth/test_broker_auth.py

def test_register_broker_invalid_route(client):
    """
    Test if registration fails for broker role when trying to register on a non-existent route.
    """
    response = client.post("/api/auth/register/invalid/broker", data={"username": "broker", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for invalid route

