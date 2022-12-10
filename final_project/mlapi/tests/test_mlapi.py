import sys
sys.path
sys.path.append('/mlapi/src/main.py')
import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from numpy.testing import assert_almost_equal
from src.main import app


@pytest.fixture
def client():
    FastAPICache.init(InMemoryBackend())
    with TestClient(app) as c:
        yield c


def test_predict(client):
    data = {"text": ["I hate you.", "I love you."]}
    response = client.post(
        "/predict",
        json=data,
    )

    assert response.status_code == 200
    assert type(response.json()["predictions"]) is list
    assert type(response.json()["predictions"][0]) is list
    assert type(response.json()["predictions"][0][0]) is dict
    assert type(response.json()["predictions"][1][0]) is dict
    assert set(response.json()["predictions"][0][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][0][1].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][1].keys()) == {"label", "score"}
    assert response.json()["predictions"][0][0]["label"] == "NEGATIVE"
    assert response.json()["predictions"][0][1]["label"] == "POSITIVE"
    assert response.json()["predictions"][1][0]["label"] == "NEGATIVE"
    assert response.json()["predictions"][1][1]["label"] == "POSITIVE"
    assert (
        assert_almost_equal(
            response.json()["predictions"][0][0]["score"], 0.936, decimal=3
        )
        is None
    )
    assert (
        assert_almost_equal(
            response.json()["predictions"][0][1]["score"], 0.064, decimal=3
        )
        is None
    )
    assert (
        assert_almost_equal(
            response.json()["predictions"][1][0]["score"], 0.003, decimal=3
        )
        is None
    )
    assert (
        assert_almost_equal(
            response.json()["predictions"][1][1]["score"], 0.997, decimal=3
        )
        is None
    )


def test_fail_get(client):
    response = client.get(
        "/predict"
    )

    assert response.status_code == 405


def test_fail_data(client):
    data = {"text": "I hate you."}
    response = client.post(
        "/predict",
        json=data,
    )

    assert response.status_code == 422



def test_fail_post_health(client):
    data = {"text": "I hate you."}
    response = client.post(
        "/health",
        json=data
    )

    assert response.status_code == 405

def test_fail_endpoint(client):
    data = {"text": "I hate you."}
    response = client.get(
        "/fake-endpoint"
    )

    assert response.status_code == 404