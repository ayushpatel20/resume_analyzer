from fastapi import status


def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "jane@example.com"
    assert data["user"]["name"] == "Jane Doe"


def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Another User",
            "email": test_user.email,
            "password": "anotherpassword",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_login_success(client, test_user):
    response = client.post(
        "/api/auth/login",
        json={
            "email": test_user.email,
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_user.email


def test_login_wrong_password(client, test_user):
    response = client.post(
        "/api/auth/login",
        json={
            "email": test_user.email,
            "password": "wrongpassword",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, auth_headers, test_user):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name


def test_unauthorized_access(client):
    response = client.get("/api/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
