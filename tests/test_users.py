from app import schemas
from .testdatabase import client, session


# Test cases
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Welcome to FASTAPI"


def test_create_user(client):
    raw_data = {
        "name": "Mum",
        "phone": "8807744555",
        "email": "mum@gmail.com",
        "password": "password123",
    }
    response = client.post("/users/register", json=raw_data)
    new_user = schemas.CreateUserResponse(**response.json())
    assert new_user.email == "mum@gmail.com"
    assert response.status_code == 201


def test_login_user(client):
    valid_credentials = {"username": "mum@gmail.com", "password": "password123"}
    response = client.post("/login", data=valid_credentials)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert "user_details" in response.json()


def test_invalid_credentials(client):
    invalid_credentials = {"username": "mum@gmail.com", "password": "password"}
    response = client.post("/login", data=invalid_credentials)
    assert response.status_code == 403  # Expecting Forbidden status code
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid Credentials"


def test_missing_username(client):
    invalid_credentials = {"password": "password"}
    response = client.post("/login", data=invalid_credentials)
    assert response.status_code == 422  # Expecting Unprocessable Entity status code
    assert "detail" in response.json()
