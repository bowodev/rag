import pytest

from app.application.knowledge.validate_upload import storage_key, validate_upload
from app.config.config import settings
from app.domain.errors import ValidationError


def test_validate_upload_accepts_pdf_txt_docx() -> None:
    assert validate_upload(
        filename="a.pdf", content_type="application/pdf", byte_size=10
    ) == "application/pdf"
    assert validate_upload(
        filename="a.txt", content_type="text/plain", byte_size=10
    ) == "text/plain"
    assert (
        validate_upload(
            filename="a.docx",
            content_type=(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ),
            byte_size=10,
        )
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


def test_validate_upload_rejects_unsupported_extension() -> None:
    with pytest.raises(ValidationError, match="unsupported file type"):
        validate_upload(filename="a.exe", content_type="application/octet-stream", byte_size=10)


def test_validate_upload_rejects_oversize() -> None:
    with pytest.raises(ValidationError, match="maximum size"):
        validate_upload(
            filename="a.pdf",
            content_type="application/pdf",
            byte_size=settings.max_upload_bytes + 1,
        )


def test_validate_upload_rejects_empty() -> None:
    with pytest.raises(ValidationError, match="empty"):
        validate_upload(filename="a.pdf", content_type="application/pdf", byte_size=0)


def test_storage_key_uses_basename() -> None:
    key = storage_key(
        tenant_id="t",
        bot_id="b",
        source_id="s",
        filename="../evil/notes.pdf",
    )
    assert key == "t/b/s/notes.pdf"
