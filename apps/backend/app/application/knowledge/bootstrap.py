from app.application.knowledge.index_source import IndexUploadedSource
from app.application.knowledge.mark_failed import MarkSourceFailedFromDlq
from app.application.knowledge.republish_processing import RepublishProcessingSources
from app.application.knowledge.search_ready_chunks import SearchReadyChunks
from app.application.knowledge.upload_source import UploadSource
from app.application.ports.bot import IBotRepo
from app.application.ports.chunk import IChunkRepo
from app.application.ports.chunk_embedding import IChunkEmbeddingRepo
from app.application.ports.embedder import Embedder
from app.application.ports.job_bus import JobBus
from app.application.ports.membership import IMembershipRepo
from app.application.ports.object_storage import ObjectStorage
from app.application.ports.source import ISourceRepo
from app.application.ports.text_extractor import TextExtractor


class KnowledgeService:
    def __init__(
        self,
        *,
        bot_repo: IBotRepo,
        membership_repo: IMembershipRepo,
        source_repo: ISourceRepo,
        storage: ObjectStorage,
        bus: JobBus,
        chunk_repo: IChunkRepo | None = None,
        embedding_repo: IChunkEmbeddingRepo | None = None,
        extractor: TextExtractor | None = None,
        embedder: Embedder | None = None,
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
        if (
            chunk_repo is not None
            and embedding_repo is not None
            and extractor is not None
            and embedder is not None
        ):
            self.index = IndexUploadedSource(
                source_repo,
                storage,
                chunk_repo,
                embedding_repo,
                extractor,
                embedder,
            )
            self.search_ready = SearchReadyChunks(embedding_repo)
