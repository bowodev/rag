from uuid import UUID

from fastapi import status

from app.application.knowledge.bootstrap import KnowledgeService
from app.cmd.api.errors import api_error
from app.domain.errors import ForbiddenError, ValidationError
from app.domain.knowledge.source import SourceDetail


class KnowledgeHTTPHandler:
    def __init__(self, knowledge_service: KnowledgeService) -> None:
        self._knowledge = knowledge_service

    async def upload(
        self,
        *,
        user_id: UUID,
        bot_id: UUID,
        filename: str,
        content_type: str,
        data: bytes,
    ) -> SourceDetail:
        try:
            return await self._knowledge.upload(
                user_id=user_id,
                bot_id=bot_id,
                filename=filename,
                content_type=content_type,
                data=data,
            )
        except ValidationError as e:
            raise api_error(
                status.HTTP_400_BAD_REQUEST,
                message="failed to upload source",
                error=str(e) or "validation failed",
            ) from e
        except ForbiddenError as e:
            raise api_error(
                status.HTTP_403_FORBIDDEN,
                message="failed to upload source",
                error=str(e) or "bot access denied",
            ) from e
        except Exception as e:
            raise api_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="failed to upload source",
                error="an unexpected error occurred",
            ) from e
