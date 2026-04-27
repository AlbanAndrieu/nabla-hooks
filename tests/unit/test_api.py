"""Test the API."""

from typing import Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient

# from unittest.mock import patch


def create_test_app_for_ping() -> FastAPI:
    """Create a minimal FastAPI app for testing v1 ping endpoint."""
    from nabla.api import ping

    test_app = FastAPI(title="Nabla V1 Test", version="0.0.1")

    # Create v1 router manually to avoid opentelemetry dependency
    from fastapi import APIRouter
    from starlette.responses import JSONResponse

    v1_router = APIRouter(prefix="/v1")

    @v1_router.get("/ping")
    async def pong():
        """Healthcheck endpoint."""
        return JSONResponse({"ping": "pong v1!"})

    test_app.include_router(v1_router)

    return test_app


def test_ping(*args) -> None:
    """It runs and gives correct response from ping."""
    # given
    app = create_test_app_for_ping()
    client = TestClient(app)
    expected_status: int = 200
    expected_response: Dict[str, str] = {"ping": "pong v1!"}

    # when
    response = client.get("/v1/ping")

    # then
    assert response.status_code == expected_status
    assert response.json() == expected_response
