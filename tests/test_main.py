import re

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.solver.data.Result import Result

client: TestClient = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "a href" in response.text


def test_get_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert re.match(r"^v([0-9]+.)+[0-9]+$", response.text) is not None


def test_get_debug():
    response = client.get("/debug")
    assert response.status_code == 200
    assert "Version" in response.text


def test_get_settings():
    response = client.get("/settings")
    assert response.status_code == 200
    assert "n_max" in response.text


def test_invalid(testjob_s, testresult_s):
    testdict = testjob_s.model_dump()
    testdict['cut_width'] = -10
    reply = client.post("/solve", json=testdict)
    assert reply.status_code != 200
    json_result = reply.json()
    with pytest.raises(ValueError, match='Field required'):
        assert Result.model_validate(json_result) == testresult_s


def test_solve_full(testjob_s, testresult_s):
    reply = client.post("/solve", json=testjob_s.model_dump())
    assert reply.status_code == 200
    json_result = reply.json()
    assert Result.model_validate(json_result) == testresult_s


def test_healthcheck_filter():
    from app.main import HealthCheckFilter
    import logging

    log_filter = HealthCheckFilter()
    health_record = logging.LogRecord(
        name="uvicorn.access", level=logging.INFO, pathname="", lineno=0,
        msg='127.0.0.1:12345 - "GET /version HTTP/1.1" 200 OK', args=(), exc_info=None
    )
    assert log_filter.filter(health_record) is False

    solve_record = logging.LogRecord(
        name="uvicorn.access", level=logging.INFO, pathname="", lineno=0,
        msg='127.0.0.1:12345 - "POST /solve HTTP/1.1" 200 OK', args=(), exc_info=None
    )
    assert log_filter.filter(solve_record) is True


def test_solve_telemetry(testjob_s, caplog):
    import logging
    with caplog.at_level(logging.INFO):
        # Standalone API call (no referer)
        client.post("/solve", json=testjob_s.model_dump())
        assert "[STANDALONE_API]" in caplog.text

        caplog.clear()
        # Web UI call (with referer)
        client.post(
            "/solve",
            json=testjob_s.model_dump(),
            headers={"referer": "https://cutsolver.modisch.me/"}
        )
        assert "[WEB_UI]" in caplog.text

