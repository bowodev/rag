from app.domain.dto.jobs import IndexSource


async def test_event_handler(message: IndexSource) -> None:
    print(f"Received message: {message}")
