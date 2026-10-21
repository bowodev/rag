import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

ERROR_RESPONSE_SCHEMA: dict[str, Any] = {
    "title": "ErrorResponse",
    "type": "object",
    "required": ["message", "error"],
    "properties": {
        "message": {
            "type": "string",
            "title": "Message",
            "example": "failed to login",
        },
        "error": {
            "type": "string",
            "title": "Error",
            "example": "Email is required",
        },
    },
}

class ErrorResponse(BaseModel):
    message: str = Field(examples=["failed to login"])
    error: str = Field(examples=["Email is required"])


def api_error(
    status_code: int,
    *,
    message: str,
    error: str,
) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=ErrorResponse(message=message, error=error).model_dump(),
    )


def _detail_to_error(detail: object) -> ErrorResponse:
    if isinstance(detail, dict) and "message" in detail and "error" in detail:
        return ErrorResponse(message=str(detail["message"]), error=str(detail["error"]))
    if isinstance(detail, list):
        parts = []
        for item in detail:
            if isinstance(item, dict) and "msg" in item:
                loc = ".".join(str(x) for x in item.get("loc", ()))
                parts.append(f"{loc}: {item['msg']}" if loc else str(item["msg"]))
            else:
                parts.append(str(item))
        return ErrorResponse(
            message="request failed",
            error="; ".join(parts) if parts else "unknown error",
        )
    return ErrorResponse(message="request failed", error=str(detail))


def _error_response_ref() -> dict[str, Any]:
    return {
        "description": "Error",
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
            }
        },
    }


def customize_openapi(app: FastAPI) -> None:
    def openapi() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        )
        components = schema.setdefault("components", {})
        schemas = components.setdefault("schemas", {})
        schemas["ErrorResponse"] = ERROR_RESPONSE_SCHEMA
        # FastAPI auto-wires 422 to HTTPValidationError — remap to our shape.
        schemas["HTTPValidationError"] = ERROR_RESPONSE_SCHEMA
        schemas.pop("ValidationError", None)

        for path_item in schema.get("paths", {}).values():
            for operation in path_item.values():
                if not isinstance(operation, dict):
                    continue
                responses = operation.setdefault("responses", {})
                for code in ("400", "401", "403", "404", "422", "500"):
                    responses[code] = _error_response_ref()

        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = openapi  # type: ignore[method-assign]


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        _request: Request, exc: HTTPException
    ) -> JSONResponse:
        body = _detail_to_error(exc.detail)
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        parts: list[str] = []
        for item in exc.errors():
            loc = ".".join(str(x) for x in item.get("loc", ()))
            msg = str(item.get("msg", "invalid"))
            parts.append(f"{loc}: {msg}" if loc else msg)
        body = ErrorResponse(
            message="failed to validate request",
            error="; ".join(parts) if parts else "invalid request",
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=body.model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        _request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("unhandled error: %s", exc)
        body = ErrorResponse(
            message="internal server error",
            error="an unexpected error occurred",
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=body.model_dump(),
        )
