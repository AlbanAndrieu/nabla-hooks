"""Test the API."""
from typing import Dict

from fastapi.testclient import TestClient

# from unittest.mock import patch


def test_ping(*args) -> None:
    """It runs and gives correct response from ping."""
    # given
    from serve import app

    client = TestClient(app)
    expected_status: int = 200
    expected_response: Dict[str, str] = {"ping": "pong v1!"}

    # when
    response = client.get("/v1/ping")

    # then
    assert response.status_code == expected_status
    assert response.json() == expected_response
