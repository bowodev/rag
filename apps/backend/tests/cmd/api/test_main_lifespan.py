from unittest.mock import AsyncMock, MagicMock, patch

from starlette.testclient import TestClient

from app.cmd.api.main import app


def test_lifespan_closes_rabbitmq_after_http_serving():
    """Shared RabbitMQ opens on startup and closes only after lifespan exits
    (after uvicorn has drained HTTP on SIGTERM/SIGINT).
    """
    mock_conn = AsyncMock()
    mock_conn.close = AsyncMock()
    mock_storage = MagicMock()
    mock_storage.ensure_bucket = AsyncMock()

    with (
        patch(
            "app.cmd.api.main.get_connection",
            new=AsyncMock(return_value=mock_conn),
        ),
        patch(
            "app.cmd.api.main.ensure_knowledge_topology",
            new=AsyncMock(),
        ),
        patch(
            "app.cmd.api.main.S3ObjectStorage",
            return_value=mock_storage,
        ),
    ):
        with TestClient(app) as client:
            response = client.get("/health")
            assert response.status_code == 200
            assert app.state.rabbitmq is mock_conn
            mock_conn.close.assert_not_called()
            mock_storage.ensure_bucket.assert_awaited()

        mock_conn.close.assert_awaited_once()
