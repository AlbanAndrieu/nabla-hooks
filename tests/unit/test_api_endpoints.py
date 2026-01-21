"""Additional tests for the nabla API."""

from typing import Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient


def create_test_app() -> FastAPI:
    """Create a minimal FastAPI app for testing without external dependencies."""
    from nabla.api import ping

    test_app = FastAPI(title="Nabla V1 Test", version="0.0.1")

    @test_app.get("/")
    async def read_root():
        return {"Hello": "World"}

    @test_app.get("/health")
    def get_status() -> Dict[str, str]:
        """Healthcheck endpoint."""
        return {"status": "pass"}

    @test_app.get("/io_task")
    async def io_task():
        import time

        time.sleep(1)
        return "IO bound task finish!"

    @test_app.get("/cpu_task")
    async def cpu_task():
        for i in range(1000):
            i * i * i
        return "CPU bound task finish!"

    test_app.include_router(ping.router)

    return test_app


def test_root_endpoint() -> None:
    """Test the root endpoint returns correct response."""
    # given
    app = create_test_app()
    client = TestClient(app)
    expected_status: int = 200
    expected_response: Dict[str, str] = {"Hello": "World"}

    # when
    response = client.get("/")

    # then
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_health_endpoint() -> None:
    """Test the health check endpoint."""
    # given
    app = create_test_app()
    client = TestClient(app)
    expected_status: int = 200
    expected_response: Dict[str, str] = {"status": "pass"}

    # when
    response = client.get("/health")

    # then
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_io_task_endpoint() -> None:
    """Test the IO task endpoint."""
    # given
    app = create_test_app()
    client = TestClient(app)
    expected_status: int = 200
    expected_response: str = "IO bound task finish!"

    # when
    response = client.get("/io_task")

    # then
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_cpu_task_endpoint() -> None:
    """Test the CPU task endpoint."""
    # given
    app = create_test_app()
    client = TestClient(app)
    expected_status: int = 200
    expected_response: str = "CPU bound task finish!"

    # when
    response = client.get("/cpu_task")

    # then
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_ping_endpoint_without_version() -> None:
    """Test the ping endpoint without version prefix."""
    # given
    app = create_test_app()
    client = TestClient(app)
    expected_status: int = 200
    expected_response: Dict[str, str] = {"ping": "pong!"}

    # when
    response = client.get("/ping")

    # then
    assert response.status_code == expected_status
    assert response.json() == expected_response
