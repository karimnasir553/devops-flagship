def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_shorten_creates_code(client):
    r = client.post("/shorten", json={"target_url": "https://example.com"})
    assert r.status_code == 201
    body = r.json()
    assert body["short_code"]
    assert body["clicks"] == 0


def test_redirect_increments_clicks(client):
    code = client.post("/shorten", json={"target_url": "https://example.com"}).json()["short_code"]
    r = client.get(f"/{code}", follow_redirects=False)
    assert r.status_code in (307, 308)
    assert "example.com" in r.headers["location"]
    assert client.get(f"/stats/{code}").json()["clicks"] == 1


def test_missing_code_returns_404(client):
    assert client.get("/stats/missing").status_code == 404
    assert client.get("/missing", follow_redirects=False).status_code == 404


def test_invalid_url_rejected(client):
    assert client.post("/shorten", json={"target_url": "not-a-url"}).status_code == 422


def test_get_db_yields_session():
    from app.database import get_db

    gen = get_db()
    db = next(gen)
    assert db is not None
    gen.close()
