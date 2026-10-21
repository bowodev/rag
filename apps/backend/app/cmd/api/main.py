import logging
from contextlib import asynccontextmanager

from app.cmd.api.errors import customize_openapi, register_exception_handlers
from app.cmd.api.routes import api_router
from app.infrastructure.rabbitmq.connection import get_connection
from app.infrastructure.rabbitmq.topology import ensure_knowledge_topology
from app.infrastructure.storage.s3 import S3ObjectStorage
from fastapi import FastAPI

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Own process resources for the API.

    Shutdown order (enforced by uvicorn, then this block):
    1. HTTP — stop accepting; drain in-flight requests (uvicorn on SIGTERM/SIGINT)
    2. Deps — close shared connections (RabbitMQ here; future DB pools, etc.)
    """
    app.state.rabbitmq = await get_connection()
    try:
        await ensure_knowledge_topology(app.state.rabbitmq)
    except Exception:
        logger.exception("failed to declare knowledge RabbitMQ topology")

    storage = S3ObjectStorage()
    try:
        await storage.ensure_bucket()
    except Exception:
        logger.exception(
            "failed to ensure s3 bucket; start MinIO (make infra-up) before uploads"
        )
    app.state.object_storage = storage

    try:
        yield
    finally:
        # Runs only after uvicorn has finished draining HTTP.
        await app.state.rabbitmq.close()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
customize_openapi(app)
app.include_router(api_router)
