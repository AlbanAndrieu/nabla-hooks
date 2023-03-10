"""Test the API."""
from typing import Dict
from unittest.mock import patch

from fastapi.testclient import TestClient


@patch("citation.infrastructure.connect_to_cloud.connect_to_cloud")
@patch("jm_ner.predict.Predict")
@patch("citation.tokenizer.spacy_tokenizer.SimpleSpacy")
@patch("citation.tokenizer.jm_tokenizer.JMTokenizer")
@patch("citation.target_categorizer.target_categorizer.TargetCategorizer")
def test_ping(*args) -> None:
    """It runs and gives correct response from ping."""
    # given
    from serve import app

    client = TestClient(app)
    expected_status: int = 200
    expected_response: Dict[str, str] = {"ping": "pong"}

    # when
    response = client.get("/citemap/ping")

    # then
    assert response.status_code == expected_status
    assert response.json() == expected_response
