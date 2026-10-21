from app.application.ports.bot import BotRecord
from app.domain.bot.summary import BotSummary


def to_bot_summary(bot: BotRecord) -> BotSummary:
    status = bot.status.value if hasattr(bot.status, "value") else str(bot.status)
    return BotSummary(
        id=bot.id,
        name=bot.name,
        status=status,
        tenant_id=bot.tenant_id,
        created_at=bot.created_at,
        updated_at=bot.updated_at,
    )
