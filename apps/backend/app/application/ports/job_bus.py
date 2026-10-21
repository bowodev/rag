from typing import Protocol

class JobBus(Protocol):
    async def publish[T](self, *, message: T) -> None: ...