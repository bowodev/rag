import io

from docx import Document
from pypdf import PdfReader

from app.domain.errors import ValidationError

_PDF = "application/pdf"
_TXT = "text/plain"
_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class FileTextExtractor:
    def extract(self, *, body: bytes, content_type: str, filename: str) -> str:
        ct = content_type.lower().split(";")[0].strip()
        if ct == _PDF or filename.lower().endswith(".pdf"):
            return self._pdf(body)
        if ct == _TXT or filename.lower().endswith(".txt"):
            return self._txt(body)
        if ct == _DOCX or filename.lower().endswith(".docx"):
            return self._docx(body)
        raise ValidationError(f"unsupported content type for extract: {content_type}")

    def _pdf(self, body: bytes) -> str:
        reader = PdfReader(io.BytesIO(body))
        pages = [(page.extract_text() or "") for page in reader.pages]
        text = "\n".join(pages).strip()
        if not text:
            raise ValidationError("pdf produced no extractable text")
        return text

    def _txt(self, body: bytes) -> str:
        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationError("txt file is not valid utf-8") from exc
        cleaned = text.strip()
        if not cleaned:
            raise ValidationError("txt file is empty")
        return cleaned

    def _docx(self, body: bytes) -> str:
        document = Document(io.BytesIO(body))
        paragraphs = [p.text for p in document.paragraphs if p.text and p.text.strip()]
        text = "\n".join(paragraphs).strip()
        if not text:
            raise ValidationError("docx produced no extractable text")
        return text
