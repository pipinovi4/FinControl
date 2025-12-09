# tests/routes/test_sessions/test_refresh_token.py

def test_refresh_token_admin(client):
    """
    Test if refresh token works for admin role.
    """
    login_response = client.post("/api/auth/login/admin/web", data={"username": "admin", "password": "password"})
    refresh_token = login_response.json()["access_token"]

    response = client.get("/api/auth/refresh/admin/web", headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_refresh_token_worker(client):
    """
    Test if refresh token works for worker role.
    """
    login_response = client.post("/api/auth/login/worker/web", data={"username": "worker", "password": "password"})
    refresh_token = login_response.json()["access_token"]

    response = client.get("/api/auth/refresh/worker/web", headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_refresh_token_broker(client):
    """
    Test if refresh token works for broker role.
    """
    login_response = client.post("/api/auth/login/broker/web", data={"username": "broker", "password": "password"})
    refresh_token = login_response.json()["access_token"]

    response = client.get("/api/auth/refresh/broker/web", headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_refresh_token_client(client):
    """
    Test if refresh token works for application role.
    """
    login_response = client.post("/api/auth/login/application/web", data={"username": "application", "password": "password"})
    refresh_token = login_response.json()["access_token"]

    response = client.get("/api/auth/refresh/application/web", headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_refresh_token_invalid(client):
    """
    Test if refresh token fails with an invalid token.
    """
    invalid_token = "invalid_token"

    response = client.get("/api/auth/refresh/admin/web", headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401  # Unauthorized
    assert response.json()["detail"] == "Invalid token"

def test_refresh_token_missing(client):
    """
    Test if refresh token fails when token is missing.
    """
    response = client.get("/api/auth/refresh/admin/web")
    assert response.status_code == 401  # Unauthorized
    assert response.json()["detail"] == "Missing token"
