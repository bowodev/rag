from openai import AsyncOpenAI

from app.config.config import settings


class OpenAIEmbedder:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        client: AsyncOpenAI | None = None,
    ) -> None:
        self._model = model or settings.embedding_model
        key = api_key if api_key is not None else settings.openai_api_key
        self._client = client or AsyncOpenAI(api_key=key or None)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = await self._client.embeddings.create(
            model=self._model,
            input=texts,
        )
        by_index = sorted(response.data, key=lambda row: row.index)
        return [list(row.embedding) for row in by_index]
