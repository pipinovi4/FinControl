# tests/routes/test_auth/test_worker_auth.py

def test_login_worker_web(client):
    """
    Test if login works for worker role on web with valid credentials.
    """
    response = client.post("/api/auth/login/worker/web", data={"username": "worker", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_worker_bot(client):
    """
    Test if login works for worker role on bot with valid credentials.
    """
    response = client.post("/api/auth/login/worker/bot", data={"username": "worker", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_worker_web(client):
    """
    Test if register works for worker role on web.
    """
    response = client.post("/api/auth/register/worker/web", data={"username": "new_worker", "password": "password"})
    assert response.status_code == 201
    assert "username" in response.json()

def test_register_worker_bot(client):
    """
    Test if register works for worker role on bot.
    """
    response = client.post("/api/auth/register/worker/bot", data={"username": "new_worker_bot", "password": "password"})
    assert response.status_code == 201
    assert "username" in response.json()

def test_login_worker_invalid_route(client):
    """
    Test if login fails for worker role when trying to log in on a non-existent route.
    """
    response = client.post("/api/auth/login/invalid/worker", data={"username": "worker", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for invalid route

def test_register_worker_invalid_route(client):
    """
    Test if registration fails for worker role when trying to register on a non-existent route.
    """
    response = client.post("/api/auth/register/invalid/worker", data={"username": "worker", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for invalid route
