import pytest


def test_valid_transfer(api_client, user_factory):
    sender = user_factory()
    receiver = user_factory()

    headers = {"Authorization": f"Bearer {sender['token']}"}

    payload = {
        "receiver_account_number": receiver["account_number"],
        "amount": 50
    }

    response = api_client.post("/transfer", data=payload, headers=headers)

    assert response.status == 200
    assert response.json()["message"] == "Transfer successful"


def test_transfer_insufficient_balance(api_client, user_factory):
    sender = user_factory()
    receiver = user_factory()

    headers = {"Authorization": f"Bearer {sender['token']}"}

    payload = {
        "receiver_account_number": receiver["account_number"],
        "amount": 999999
    }

    response = api_client.post("/transfer", data=payload, headers=headers)

    assert response.status == 400
    assert response.json()["message"] == "Insufficient balance"


def test_transfer_to_self(api_client, user_factory):
    user = user_factory()

    headers = {"Authorization": f"Bearer {user['token']}"}

    payload = {
        "receiver_account_number": user["account_number"],
        "amount": 10
    }

    response = api_client.post("/transfer", data=payload, headers=headers)

    assert response.status == 400
    assert response.json()["message"] == "Cannot transfer to same account"


@pytest.mark.parametrize("amount", [-10, 0])
def test_invalid_amount(api_client, user_factory, amount):
    sender = user_factory()
    receiver = user_factory()

    headers = {"Authorization": f"Bearer {sender['token']}"}

    payload = {
        "receiver_account_number": receiver["account_number"],
        "amount": amount
    }

    response = api_client.post("/transfer", data=payload, headers=headers)

    assert response.status == 400
    assert response.json()["message"] == "Amount must be greater than 0"


def test_transfer_missing_fields(api_client, user_factory):
    user = user_factory()

    headers = {"Authorization": f"Bearer {user['token']}"}

    response = api_client.post("/transfer", data={}, headers=headers)

    assert response.status == 400
    assert response.json()["message"] == "All fields are required"