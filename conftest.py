import pytest
import random
import string
from utils.api_client import APIClient

from config.settings import BASE_URL

def random_email():
    return "test_" + "".join(random.choices(string.ascii_lowercase, k=6)) + "@test.com"


@pytest.fixture(scope="session")
def api_client():
    return APIClient(BASE_URL)


# ===============================
# USER FACTORY
# ===============================
@pytest.fixture
def user_factory(api_client):
    def create_user():
        email = random_email()
        password = "Test@123"

        # Register
        api_client.post("/register", data={
            "full_name": "Automation User",
            "email": email,
            "password": password
        })

        # Login
        login = api_client.post("/login", data={
            "email": email,
            "password": password
        })

        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get account number
        me = api_client.get("/me", headers=headers)

        account_number = me.json()["account_number"]

        return {
            "email": email,
            "password": password,
            "token": token,
            "account_number": account_number
        }

    return create_user