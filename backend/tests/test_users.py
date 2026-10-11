async def test_me_requires_auth(client):
    response = await client.get("/api/users/me")
    assert response.status_code == 401


async def test_me_returns_current_user(client, register_and_login, user_payload):
    token = await register_and_login(user_payload)
    response = await client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "alice"
    assert body["email"] == "alice@example.com"


async def test_me_rejects_invalid_token(client):
    response = await client.get("/api/users/me", headers={"Authorization": "Bearer not-a-jwt"})
    assert response.status_code == 401


async def test_update_profile(client, register_and_login, user_payload):
    token = await register_and_login(user_payload)
    response = await client.put(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "Alice B", "bio": "hello world"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["full_name"] == "Alice B"
    assert body["bio"] == "hello world"


async def test_get_user_by_id(client, register_and_login, user_payload):
    token = await register_and_login(user_payload)
    me = (await client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})).json()
    response = await client.get(f"/api/users/{me['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == me["id"]


async def test_get_user_not_found(client):
    response = await client.get("/api/users/99999")
    assert response.status_code == 404