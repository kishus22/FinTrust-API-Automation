import pytest


def test_user_login_success(api_client, user_factory):
    user = user_factory()

    response = api_client.post("/login", data={
        "email": user["email"],
        "password": user["password"]
    })

    assert response.status == 200
    assert "access_token" in response.json()


def test_invalid_password(api_client, user_factory):
    user = user_factory()

    response = api_client.post("/login", data={
        "email": user["email"],
        "password": "WrongPassword"
    })

    assert response.status == 401
    assert response.json()["message"] == "Invalid credentials"


def test_invalid_email(api_client):
    response = api_client.post("/login", data={
        "email": "fake@test.com",
        "password": "Test@123"
    })

    assert response.status == 401
    assert response.json()["message"] == "Invalid credentials"


@pytest.mark.parametrize("payload", [
    {"email": "", "password": "Test@123"},
    {"email": "test@test.com", "password": ""},
    {}
])
def test_missing_fields(api_client, payload):
    response = api_client.post("/login", data=payload)

    assert response.status == 400