from contextlib import asynccontextmanager

from app.cmd.api.errors import customize_openapi, register_exception_handlers
from app.cmd.api.routes import api_router
from app.infrastructure.rabbitmq.connection import get_connection
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Own process resources for the API.

    Shutdown order (enforced by uvicorn, then this block):
    1. HTTP — stop accepting; drain in-flight requests (uvicorn on SIGTERM/SIGINT)
    2. Deps — close shared connections (RabbitMQ here; future DB pools, etc.)
    """
    app.state.rabbitmq = await get_connection()
    try:
        yield
    finally:
        # Runs only after uvicorn has finished draining HTTP.
        await app.state.rabbitmq.close()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
customize_openapi(app)
app.include_router(api_router)
