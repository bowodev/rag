"""Shared test fixtures.

API TestClient runs FastAPI lifespan; mock MinIO bucket ensure so suites
do not require a live object store.
"""

from collections.abc import Iterator
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture(autouse=True)
def _mock_s3_ensure_bucket() -> Iterator[None]:
    with patch(
        "app.cmd.api.main.S3ObjectStorage.ensure_bucket",
        new=AsyncMock(),
    ):
        yield
