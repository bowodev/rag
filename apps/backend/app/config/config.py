from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "vcs-backend"
    database_url: str = "postgresql+asyncpg://vcs:vcs@localhost:5432/vcs"
    rabbitmq_url: str = "amqp://vcs:vcs@localhost:5672/"
    knowledge_queue: str = "knowledge.index"
    knowledge_dlq: str = "knowledge.index.dlq"
    knowledge_dlx: str = "knowledge.index.dlx"
    knowledge_recovery_queue: str = "knowledge.recovery"
    knowledge_recovery_interval_seconds: float = 60.0
    knowledge_recovery_min_age_seconds: float = 30.0
    embedding_dimension: int = 1536
    jwt_secret: str = "change-me"  # wajib override di .env
    jwt_algorithm: str = "HS256"
    jwt_ttl_seconds: int = 3600
    jwt_refresh_ttl_seconds: int = 604800  # 7 days

    # MinIO / S3-compatible object storage
    s3_endpoint_url: str = "http://127.0.0.1:9000"
    s3_access_key: str = "vcs"
    s3_secret_key: str = "vcschangeme"
    s3_bucket: str = "vcs-knowledge"
    s3_region: str = "us-east-1"
    max_upload_bytes: int = 10 * 1024 * 1024  # 10 MB


settings = Settings()
