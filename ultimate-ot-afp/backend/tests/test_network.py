def test_network_status():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    r = client.get("/api/v1/network/status")
    assert r.status_code == 200
