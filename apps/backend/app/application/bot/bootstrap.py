from app.application.bot.get_for_user import GetBotForUser
from app.application.bot.list_for_user import ListBotsForUser
from app.application.ports.bot import IBotRepo
from app.application.ports.membership import IMembershipRepo


class BotService:
    def __init__(
        self,
        *,
        bot_repo: IBotRepo,
        membership_repo: IMembershipRepo,
    ) -> None:
        self.list_for_user = ListBotsForUser(bot_repo, membership_repo)
        self.get_for_user = GetBotForUser(bot_repo, membership_repo)
