from io import BytesIO

import pytest
from docx import Document

from app.domain.errors import ValidationError
from app.infrastructure.knowledge.extract import FileTextExtractor


def test_extract_txt() -> None:
    text = FileTextExtractor().extract(
        body=b"hello knowledge",
        content_type="text/plain",
        filename="a.txt",
    )
    assert text == "hello knowledge"


def test_extract_txt_rejects_empty() -> None:
    with pytest.raises(ValidationError):
        FileTextExtractor().extract(
            body=b"   ",
            content_type="text/plain",
            filename="a.txt",
        )


def test_extract_docx() -> None:
    buf = BytesIO()
    doc = Document()
    doc.add_paragraph("Docx body line")
    doc.save(buf)
    text = FileTextExtractor().extract(
        body=buf.getvalue(),
        content_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
        filename="a.docx",
    )
    assert "Docx body line" in text
