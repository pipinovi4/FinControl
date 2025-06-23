# tests/routes/test_auth/test_admin_auth.py

def test_login_admin_web(client):
    """
    Test if login works for admin role on web with valid credentials.
    """
    response = client.post("/api/auth/login/admin/web", data={"username": "admin", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_admin_bot(client):
    """
    Test if login works for admin role on bot with valid credentials.
    """
    response = client.post("/api/auth/login/admin/bot", data={"username": "admin_bot", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_admin_web(client):
    """
    Test if register works for admin role on web.
    """
    response = client.post("/api/auth/register/admin/web", data={"username": "new_admin", "password": "password"})
    assert response.status_code == 201
    assert "username" in response.json()

def test_register_admin_bot(client):
    """
    Test if register works for admin role on bot.
    """
    response = client.post("/api/auth/register/admin/bot", data={"username": "new_admin_bot", "password": "password"})
    assert response.status_code == 201
    assert "username" in response.json()

def test_login_admin_invalid_route(client):
    """
    Test if login fails for admin role when trying to log   in on a non-existent route.
    """
    response = client.post("/api/auth/login/invalid/admin", data={"username": "admin", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for invalid route

def test_register_admin_invalid_route(client):
    """
    Test if registration fails for admin role when trying to register on a non-existent route.
    """
    response = client.post("/api/auth/register/invalid/admin", data={"username": "admin", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for invalid route
