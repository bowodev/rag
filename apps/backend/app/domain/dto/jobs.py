from pydantic import BaseModel
from uuid import UUID

class IndexSource(BaseModel):
    source_id: UUID
    tenant_id: UUID
    bot_id: UUID