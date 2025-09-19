# tests/routes/test_system.py
def test_ping(client):
    """
    Test if the /ping route is returning the correct status.
    """
    response = client.get("/api/system/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Backend is alive"}

def test_routes_info(client):
    """
    Test if the /routes-info endpoint returns all registered routes.
    """
    response = client.get("/api/system/routes-info")
    assert response.status_code == 200
    assert "endpoints" in response.json()
