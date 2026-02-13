import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    # Signup
    email = "testuser@mergington.edu"
    activity = "Basketball Team"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200 or signup_resp.status_code == 400
    # Unregister
    unregister_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200 or unregister_resp.status_code == 404

def test_signup_duplicate():
    email = "james@mergington.edu"
    activity = "Basketball Team"
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json().get("detail", "")

def test_unregister_not_found():
    email = "notfound@mergington.edu"
    activity = "Basketball Team"
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 404
    assert "Participant not found" in resp.json().get("detail", "")
