def test_customer_cannot_view_users(api_client, user_factory):
    user = user_factory()

    headers = {"Authorization": f"Bearer {user['token']}"}

    response = api_client.get("/users", headers=headers)

    assert response.status == 403


def test_customer_cannot_block_user(api_client, user_factory):
    user = user_factory()

    headers = {"Authorization": f"Bearer {user['token']}"}

    response = api_client.patch("/block-user/1", headers=headers)

    assert response.status == 403