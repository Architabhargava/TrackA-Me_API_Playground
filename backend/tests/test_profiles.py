from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200

def test_unauthorized_create():
    res = client.post("/profile", json={})
    assert res.status_code == 401

def test_search_skill():
    res = client.get("/profiles/search?skill=ai")
    assert res.status_code == 200

