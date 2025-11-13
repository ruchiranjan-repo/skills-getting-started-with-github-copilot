import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    activity = "Chess Club"
    email = "pytestuser@mergington.edu"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Signup
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response_unreg.status_code == 200
    assert f"Unregistered {email}" in response_unreg.json()["message"]
    # Try duplicate unregister
    response_unreg2 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response_unreg2.status_code == 400

def test_signup_activity_not_found():
    response = client.post("/activities/NonexistentActivity/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.delete("/activities/NonexistentActivity/unregister", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
