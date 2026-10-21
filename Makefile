.PHONY: help infra-up infra-down infra-ps infra-logs \
	backend-install backend-api backend-consumer backend-test \
	publish-test

BACKEND_DIR := apps/backend
API_HOST := 127.0.0.1
API_PORT := 8000

help:
	@echo "Infra"
	@echo "  make infra-up       Start Postgres + RabbitMQ"
	@echo "  make infra-down     Stop infra"
	@echo "  make infra-ps       Show infra status"
	@echo "  make infra-logs     Tail infra logs"
	@echo ""
	@echo "Backend"
	@echo "  make backend-install   Install Python deps (uv)"
	@echo "  make backend-api       Run FastAPI (reload)"
	@echo "  make backend-consumer  Run RabbitMQ consumer (default: test)"
	@echo "  make backend-consumer-list  List available consumers"
	@echo "  make backend-test      Run pytest"
	@echo "  make publish-test      POST /test-publish smoke"

infra-up:
	docker compose up -d

infra-down:
	docker compose down

infra-ps:
	docker compose ps

infra-logs:
	docker compose logs -f

backend-install:
	cd $(BACKEND_DIR) && uv sync

backend-api:
	cd $(BACKEND_DIR) && uv run uvicorn app.cmd.api.main:app --reload --host $(API_HOST) --port $(API_PORT)

backend-consumer-test:
	cd $(BACKEND_DIR) && uv run python -m app.cmd.consumer.main test

backend-consumer-list:
	cd $(BACKEND_DIR) && uv run python -m app.cmd.consumer.main --list

backend-test:
	cd $(BACKEND_DIR) && uv run pytest

publish-test:
	curl -sS -X POST http://$(API_HOST):$(API_PORT)/test-publish
	@echo
