def test_autonomous_status():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    r = client.get("/api/v1/autonomous/status")
    assert r.status_code == 200
