from fastapi.testclient import TestClient

from app.main import app

client: TestClient = TestClient(app)


def test_get_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.text == "0.2"
