from pathlib import PurePosixPath

from app.config.config import settings
from app.domain.errors import ValidationError

_CANONICAL_TYPE: dict[str, str] = {
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".docx": (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ),
}


def validate_upload(*, filename: str, content_type: str, byte_size: int) -> str:
    """Validate size/extension; return canonical content_type."""
    if byte_size <= 0:
        raise ValidationError("file is empty")
    if byte_size > settings.max_upload_bytes:
        raise ValidationError(
            f"file exceeds maximum size of {settings.max_upload_bytes} bytes"
        )

    suffix = PurePosixPath(filename).suffix.lower()
    canonical = _CANONICAL_TYPE.get(suffix)
    if canonical is None:
        raise ValidationError("unsupported file type; allowed: pdf, txt, docx")

    normalized = (content_type or "").split(";")[0].strip().lower()
    if (
        normalized
        and normalized not in (canonical, "application/octet-stream")
        and not (suffix == ".txt" and normalized.startswith("text/"))
    ):
        raise ValidationError(
            "unsupported content type for file extension; allowed: pdf, txt, docx"
        )

    return canonical


def storage_key(*, tenant_id: str, bot_id: str, source_id: str, filename: str) -> str:
    safe = PurePosixPath(filename).name.replace("..", "_")
    return f"{tenant_id}/{bot_id}/{source_id}/{safe}"
