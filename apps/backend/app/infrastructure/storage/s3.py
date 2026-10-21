import logging

import aioboto3
from botocore.config import Config
from botocore.exceptions import ClientError

from app.config.config import settings

logger = logging.getLogger(__name__)

_S3_CONFIG = Config(
    connect_timeout=2,
    read_timeout=5,
    retries={"max_attempts": 1},
    s3={"addressing_style": "path"},
)


class S3ObjectStorage:
    def __init__(
        self,
        *,
        endpoint_url: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
        bucket: str | None = None,
        region: str | None = None,
    ) -> None:
        self._endpoint_url = endpoint_url or settings.s3_endpoint_url
        self._access_key = access_key or settings.s3_access_key
        self._secret_key = secret_key or settings.s3_secret_key
        self._bucket = bucket or settings.s3_bucket
        self._region = region or settings.s3_region
        self._session = aioboto3.Session()

    def _client_kwargs(self) -> dict[str, object]:
        return {
            "service_name": "s3",
            "endpoint_url": self._endpoint_url,
            "aws_access_key_id": self._access_key,
            "aws_secret_access_key": self._secret_key,
            "region_name": self._region,
            "config": _S3_CONFIG,
        }

    async def ensure_bucket(self) -> None:
        async with self._session.client(**self._client_kwargs()) as client:
            try:
                await client.head_bucket(Bucket=self._bucket)
            except ClientError:
                logger.info("creating s3 bucket %s", self._bucket)
                await client.create_bucket(Bucket=self._bucket)

    async def put(
        self,
        *,
        key: str,
        body: bytes,
        content_type: str,
    ) -> None:
        async with self._session.client(**self._client_kwargs()) as client:
            await client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=body,
                ContentType=content_type,
            )

    async def delete(self, *, key: str) -> None:
        async with self._session.client(**self._client_kwargs()) as client:
            await client.delete_object(Bucket=self._bucket, Key=key)
