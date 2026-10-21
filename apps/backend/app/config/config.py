from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "vcs-backend"
    database_url: str = "postgresql+asyncpg://vcs:vcs@localhost:5432/vcs"
    rabbitmq_url: str = "amqp://vcs:vcs@localhost:5672/"
    knowledge_queue: str = "knowledge.index"
    embedding_dimension: int = 1536
    jwt_secret: str = "change-me"  # wajib override di .env
    jwt_algorithm: str = "HS256"
    jwt_ttl_seconds: int = 3600
    jwt_refresh_ttl_seconds: int = 604800  # 7 days


settings = Settings()
