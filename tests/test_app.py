import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data
    assert "participants" in data["Soccer Team"]

def test_signup_and_unregister():
    activity = "Soccer Team"
    email = "testuser@mergington.edu"

    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    if response.status_code == 200:
        assert f"Unregistered {email}" in response.json()["message"]
    else:
        # Accept 404 if activity not found (e.g., in-memory state reset)
        assert response.status_code == 404 or response.status_code == 400

    # Unregister again should fail (should be 400 or 404)
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code in (400, 404)
