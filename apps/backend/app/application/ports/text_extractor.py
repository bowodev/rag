from typing import Protocol


class TextExtractor(Protocol):
    def extract(self, *, body: bytes, content_type: str, filename: str) -> str: ...
