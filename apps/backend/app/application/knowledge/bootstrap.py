from app.application.knowledge.mark_failed import MarkSourceFailedFromDlq
from app.application.knowledge.republish_processing import RepublishProcessingSources
from app.application.knowledge.upload_source import UploadSource
from app.application.ports.bot import IBotRepo
from app.application.ports.job_bus import JobBus
from app.application.ports.membership import IMembershipRepo
from app.application.ports.object_storage import ObjectStorage
from app.application.ports.source import ISourceRepo


class KnowledgeService:
    def __init__(
        self,
        *,
        bot_repo: IBotRepo,
        membership_repo: IMembershipRepo,
        source_repo: ISourceRepo,
        storage: ObjectStorage,
        bus: JobBus,
    ) -> None:
        self.upload = UploadSource(
            bot_repo,
            membership_repo,
            source_repo,
            storage,
            bus,
        )
        self.republish_processing = RepublishProcessingSources(source_repo, bus)
        self.mark_failed_from_dlq = MarkSourceFailedFromDlq(source_repo)
