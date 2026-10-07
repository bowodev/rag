# Backend reference (FastAPI / clean code)

## Suggested use-case shape

```python
class UploadSource:
    def __init__(self, sources: SourceRepo, storage: ObjectStorage, bus: JobBus):
        self.sources = sources
        self.storage = storage
        self.bus = bus

    async def execute(self, *, tenant_id: str, bot_id: str, file) -> Source:
        # verify bot belongs to tenant
        # store raw file
        # create Source(status="processing")
        # enqueue indexing job
        # return source
```

## Router thinness

```python
@router.post("/bots/{bot_id}/sources")
async def upload_source(bot_id: str, file: UploadFile, user=Depends(auth), uc=Depends(get_upload_uc)):
    return await uc.execute(tenant_id=user.tenant_id, bot_id=bot_id, file=file)
```

## Multi-tenant query rule

Always pass tenant (and bot when applicable) into repositories. Never load by id alone without ownership checks.

## Knowledge processing

Treat extract/chunk/embed as infrastructure + application workflow updating Source status. Do not introduce an “IngestionJob” product domain unless docs change.
