async def test_register_and_login(client, user_payload):
    response = await client.post("/api/auth/register", json=user_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert body["username"] == "alice"
    assert body["full_name"] == "Alice Example"
    assert "hashed_password" not in body

    duplicate = await client.post("/api/auth/register", json=user_payload)
    assert duplicate.status_code == 400
    assert "email already exists" in duplicate.json()["detail"]

    login = await client.post(
        "/api/auth/login",
        data={"username": "alice", "password": "secret123"},
    )
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    assert login.json()["access_token"]

    wrong = await client.post(
        "/api/auth/login",
        data={"username": "alice", "password": "wrong-password"},
    )
    assert wrong.status_code == 401


async def test_register_rejects_short_password(client, user_payload):
    user_payload["password"] = "abc"
    response = await client.post("/api/auth/register", json=user_payload)
    assert response.status_code == 422


async def test_register_rejects_duplicate_username(client, user_payload):
    other = dict(user_payload, email="another@example.com")
    assert (await client.post("/api/auth/register", json=user_payload)).status_code == 200
    response = await client.post("/api/auth/register", json=other)
    assert response.status_code == 400
    assert "username already exists" in response.json()["detail"]