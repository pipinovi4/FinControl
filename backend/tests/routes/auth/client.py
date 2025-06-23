# tests/routes/test_auth/test_client_auth.py

def test_login_client(client):
    """
    Test if login works for client role with valid credentials.
    """
    response = client.post("/api/auth/login/client/web", data={"username": "client", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_client(client):
    """
    Test if register works for client role.
    """
    response = client.post("/api/auth/register/client/web", data={"username": "new_client", "password": "password"})
    assert response.status_code == 201
    assert "username" in response.json()

def test_login_client_invalid_credentials(client):
    """
    Test if login fails for client role with invalid credentials.
    """
    response = client.post("/api/auth/login/client/web", data={"username": "client", "password": "wrongpassword"})
    assert response.status_code == 401
    assert "detail" in response.json()  # Expected error message for invalid credentials

def test_register_client_existing_username(client):
    """
    Test if registration fails for client role with an already existing username.
    """
    # First, register a client
    client.post("/api/auth/register/client/web", data={"username": "existing_client", "password": "password"})

    # Now try to register the same username again
    response = client.post("/api/auth/register/client/web",
                           data={"username": "existing_client", "password": "newpassword"})
    assert response.status_code == 400
    assert "detail" in response.json()  # Expected error message for existing username

def test_login_client_invalid_route(client):
    """
    Test if login fails for client role when trying to log in on a non-existent route.
    """
    response = client.post("/api/auth/login/invalid/client", data={"username": "client", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for invalid route

def test_register_client_invalid_route(client):
    """
    Test if registration fails for client role when trying to register on a non-existent route.
    """
    response = client.post("/api/auth/register/invalid/client", data={"username": "client", "password": "password"})
    assert response.status_code == 404  # Expected 404 not found for invalid route
