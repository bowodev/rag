from app.application.ports.chunk import ChunkPiece
from app.config.config import settings

_SEPARATORS = ("\n\n", "\n", " ", "")


def chunk_text(
    text: str,
    *,
    size: int | None = None,
    overlap: int | None = None,
) -> list[ChunkPiece]:
    """Fast recursive character splitter with overlap."""
    cleaned = text.strip()
    if not cleaned:
        return []

    chunk_size = size if size is not None else settings.chunk_size_chars
    chunk_overlap = overlap if overlap is not None else settings.chunk_overlap_chars
    if chunk_size <= 0:
        raise ValueError("chunk size must be positive")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk overlap must be >= 0 and < chunk size")

    parts = _split(cleaned, chunk_size)
    if not parts:
        return []

    merged = _merge_with_overlap(parts, chunk_size, chunk_overlap)
    return [
        ChunkPiece(ordinal=i, content=piece, token_count=None)
        for i, piece in enumerate(merged)
    ]


def _split(text: str, chunk_size: int) -> list[str]:
    if len(text) <= chunk_size:
        return [text]

    for sep in _SEPARATORS:
        if sep == "":
            return [
                text[i : i + chunk_size] for i in range(0, len(text), chunk_size)
            ]
        if sep not in text:
            continue
        pieces: list[str] = []
        for part in text.split(sep):
            part = part.strip() if sep != " " else part
            if not part:
                continue
            if len(part) <= chunk_size:
                pieces.append(part)
            else:
                pieces.extend(_split(part, chunk_size))
        if pieces:
            return pieces
    return [text]


def _merge_with_overlap(
    parts: list[str],
    chunk_size: int,
    overlap: int,
) -> list[str]:
    chunks: list[str] = []
    current = ""
    for part in parts:
        candidate = part if not current else f"{current} {part}".strip()
        if len(candidate) <= chunk_size:
            current = candidate
            continue
        if current:
            chunks.append(current)
            if overlap > 0:
                current = f"{current[-overlap:]} {part}".strip()
                if len(current) > chunk_size:
                    current = part
            else:
                current = part
        else:
            chunks.append(part[:chunk_size])
            current = part[chunk_size - overlap :] if overlap else part[chunk_size:]
            current = current.lstrip()
    if current:
        chunks.append(current)
    return chunks
