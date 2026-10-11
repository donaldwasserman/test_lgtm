from app.core.security import get_password_hash
from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole


async def create_user(username: str, email: str, password: str, role: UserRole = UserRole.attendee) -> User:
    async with AsyncSessionLocal() as db:
        user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            role=role,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


async def login(client, username: str, password: str) -> str:
    response = await client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


EVENT_PAYLOAD = {
    "title": "PyCon 2026",
    "description": "The annual Python conference",
    "short_description": "Python",
    "start_date": "2026-06-01T09:00:00+00:00",
    "end_date": "2026-06-03T18:00:00+00:00",
    "timezone": "UTC",
}


async def test_list_events_empty(client):
    response = await client.get("/api/events/")
    assert response.status_code == 200
    assert response.json() == []


async def test_read_event_not_found(client):
    response = await client.get("/api/events/99999")
    assert response.status_code == 404


async def test_create_event_requires_auth(client):
    response = await client.post("/api/events/", json=EVENT_PAYLOAD)
    assert response.status_code == 401


async def test_attendee_cannot_create_event(client):
    await create_user("attendee", "attendee@example.com", "secret123")
    token = await login(client, "attendee", "secret123")
    response = await client.post(
        "/api/events/",
        headers={"Authorization": f"Bearer {token}"},
        json=EVENT_PAYLOAD,
    )
    assert response.status_code == 403


async def test_organizer_creates_event(client):
    await create_user("organizer", "organizer@example.com", "secret123", UserRole.organizer)
    token = await login(client, "organizer", "secret123")

    created = await client.post(
        "/api/events/",
        headers={"Authorization": f"Bearer {token}"},
        json=EVENT_PAYLOAD,
    )
    assert created.status_code == 200
    body = created.json()
    assert body["title"] == "PyCon 2026"
    assert body["slug"] == "pycon-2026"
    assert body["status"] == "draft"
    assert body["view_count"] == 0

    listed = await client.get("/api/events/")
    assert listed.status_code == 200
    assert listed.json() == []  # drafts are not listed

    detail = await client.get(f"/api/events/{body['id']}")
    assert detail.status_code == 200
    assert detail.json()["view_count"] == 1


async def test_duplicate_event_slug_gets_suffix(client):
    await create_user("organizer2", "organizer2@example.com", "secret123", UserRole.organizer)
    token = await login(client, "organizer2", "secret123")
    headers = {"Authorization": f"Bearer {token}"}

    first = await client.post("/api/events/", headers=headers, json=EVENT_PAYLOAD)
    second = await client.post("/api/events/", headers=headers, json=EVENT_PAYLOAD)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["slug"] == "pycon-2026"
    assert second.json()["slug"] == "pycon-2026-1"