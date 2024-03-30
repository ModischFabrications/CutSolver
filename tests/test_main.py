import re

from fastapi.testclient import TestClient

from app.main import app
from app.solver.data.Result import Result
from tests.test_fixtures import testjob_s, testresult_s

client: TestClient = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert any(response.text)


def test_get_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert re.match(r"^v([0-9]+.)+[0-9]+$", response.text) is not None


def test_get_debug():
    response = client.get("/debug")
    assert response.status_code == 200
    assert any(response.text)


def test_full(testjob_s, testresult_s):
    reply = client.post("/solve", json=testjob_s.model_dump())
    assert reply.status_code == 200
    json_result = reply.json()
    assert Result.model_validate(json_result) == testresult_s
