from app.infrastructure.knowledge.chunker import chunk_text


def test_chunk_text_empty() -> None:
    assert chunk_text("   ") == []


def test_chunk_text_short_single_piece() -> None:
    pieces = chunk_text("hello world", size=100, overlap=10)
    assert len(pieces) == 1
    assert pieces[0].ordinal == 0
    assert pieces[0].content == "hello world"


def test_chunk_text_splits_long_text() -> None:
    text = "alpha\n\n" + ("word " * 80)
    pieces = chunk_text(text, size=40, overlap=5)
    assert len(pieces) > 1
    assert [p.ordinal for p in pieces] == list(range(len(pieces)))
    assert all(len(p.content) <= 45 for p in pieces)
