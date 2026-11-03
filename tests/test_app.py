"""Integration tests for the Flask frontend and JSON API."""

import pytest

from app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_homepage_lists_functions(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Functional Testing Playground" in response.data
    assert b"is_adult" in response.data
    assert b"average" in response.data


def test_health_endpoint_returns_commit_sha(client, monkeypatch):
    monkeypatch.setenv("RENDER_GIT_COMMIT", "abc123")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "commit_sha": "abc123"}


def test_health_endpoint_uses_local_fallback(client, monkeypatch):
    monkeypatch.delenv("RENDER_GIT_COMMIT", raising=False)
    monkeypatch.delenv("GITHUB_SHA", raising=False)
    assert client.get("/health").get_json()["commit_sha"] == "local"


def test_api_returns_function_result_and_type(client):
    response = client.post("/api/run", json={"function": "is_adult", "args": [18]})
    assert response.status_code == 200
    assert response.get_json() == {
        "function": "is_adult",
        "result": True,
        "result_type": "bool",
    }


def test_api_serializes_set_results(client):
    response = client.post(
        "/api/run",
        json={"function": "common_items", "args": [[1, 2, 3], [2, 3, 4]]},
    )
    assert response.status_code == 200
    assert response.get_json()["result"] == [2, 3]


def test_api_returns_target_exception(client):
    response = client.post("/api/run", json={"function": "square_root", "args": [-1]})
    assert response.status_code == 400
    assert response.get_json()["error"] == "ValueError"


def test_api_rejects_non_object_payload(client):
    response = client.post("/api/run", data="[]", content_type="application/json")
    assert response.status_code == 400
    assert "JSON object" in response.get_json()["error"]


def test_api_rejects_unknown_function(client):
    response = client.post("/api/run", json={"function": "not_a_function", "args": []})
    assert response.status_code == 400
    assert "16 available functions" in response.get_json()["error"]


def test_api_rejects_invalid_argument_containers(client):
    response = client.post(
        "/api/run", json={"function": "greet", "args": "student", "kwargs": []}
    )
    assert response.status_code == 400
    assert "args" in response.get_json()["error"]


def test_api_shows_complex_results_as_text(client):
    response = client.post("/api/run", json={"function": "power", "args": [-8, 0.5]})
    assert response.status_code == 200
    body = response.get_json()
    assert body["result_type"] == "complex"
    assert isinstance(body["result"], str)


def test_api_shows_non_finite_floats_as_valid_json(client):
    response = client.post(
        "/api/run", json={"function": "divide", "args": [1e308, 1e-308]}
    )
    assert response.status_code == 200
    assert response.get_json()["result"] == "inf"
    assert b"Infinity" not in response.data
