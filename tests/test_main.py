import re

from fastapi.testclient import TestClient

from app.main import app
from app.solver.data.Result import Result
from tests.test_utils import generate_testjob, generate_testresult

client: TestClient = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200


def test_get_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert re.match(r"^v([0-9]+.)+[0-9]$", response.text) is not None


def test_get_debug():
    response = client.get("/debug")
    assert response.status_code == 200


def test_full():
    reply = client.post("/solve", generate_testjob().json())
    assert reply.status_code == 200
    json_result = reply.json()

    assert Result.parse_obj(json_result) == generate_testresult()
