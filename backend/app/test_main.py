from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_users_me():
    response = client.get("/api/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_create_user():
    response = client.post("/api/users", json={"username": "test", "email": "test@email.com", "password": "test"})
    assert response.status_code == 200