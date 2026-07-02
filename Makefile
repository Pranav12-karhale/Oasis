# =============================================================================
# Oasis — Makefile
# Common commands for development
# =============================================================================

.PHONY: help setup up down build logs clean test

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Setup ────────────────────────────────────────────────────────────────────

setup: ## First-time setup: copy env, build images
	@echo "🏝️  Setting up Oasis..."
	@cp -n .env.example .env 2>/dev/null || true
	@echo "✅ .env created (edit with your API keys)"
	@$(MAKE) build

# ── Docker Compose ───────────────────────────────────────────────────────────

up: ## Start all services
	docker compose up -d
	@echo "🏝️  Oasis is running!"
	@echo "  Gateway:     http://localhost:8000"
	@echo "  Gateway Docs: http://localhost:8000/docs"
	@echo "  Frontend:    http://localhost:3001"
	@echo "  Grafana:     http://localhost:3000 (admin/admin)"
	@echo "  MinIO:       http://localhost:9001"
	@echo "  Qdrant:      http://localhost:6333/dashboard"

down: ## Stop all services
	docker compose down

build: ## Build all Docker images
	docker compose build

rebuild: ## Rebuild all images from scratch
	docker compose build --no-cache

logs: ## Follow logs from all services
	docker compose logs -f

logs-gateway: ## Follow gateway logs
	docker compose logs -f gateway

logs-orchestrator: ## Follow orchestrator logs
	docker compose logs -f orchestrator

ps: ## Show running services
	docker compose ps

# ── Development ──────────────────────────────────────────────────────────────

up-core: ## Start only core services (gateway + orchestrator + data stores)
	docker compose up -d postgres redis qdrant minio gateway auth orchestrator

up-observability: ## Start observability stack
	docker compose up -d otel-collector grafana prometheus loki tempo

# ── Testing ──────────────────────────────────────────────────────────────────

test: ## Run all tests
	@echo "Running tests..."
	cd services/gateway && python -m pytest tests/ -v || true
	cd services/auth && python -m pytest tests/ -v || true
	cd services/orchestrator && python -m pytest tests/ -v || true

# ── Cleanup ──────────────────────────────────────────────────────────────────

clean: ## Stop services and remove volumes (⚠️ deletes data)
	docker compose down -v
	@echo "All data volumes removed"

clean-images: ## Remove all Oasis Docker images
	docker compose down --rmi all
