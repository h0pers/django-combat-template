COMPOSE_TEST = docker compose -f docker-compose.test.yml
COMPOSE_DEBUG = docker compose -f docker-compose.debug.yml
MIGRATION_APPS = users{% if cookiecutter.use_drf == "y" or cookiecutter.use_vue == "y" %} polls{% endif %}

.PHONY: help up-debug test-image test coverage test-down lint format makemigrations migrate-check

help: ## Show available commands
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "%-16s %s\n", $$1, $$2}'

up-debug: ## Run the dev stack with hot reload at http://localhost
	$(COMPOSE_DEBUG) up --build

test-image: ## Build the test image (needed after dependency changes)
	docker build --target test -t backend:test .

test: ## Run tests; pass ARGS to select, e.g. make test ARGS=apps/core/tests/test_django_mode.py
	@docker image inspect backend:test >/dev/null 2>&1 || $(MAKE) test-image
	$(COMPOSE_TEST) run --rm test pytest $(ARGS)

coverage: ## Run tests with a coverage report
	@docker image inspect backend:test >/dev/null 2>&1 || $(MAKE) test-image
	$(COMPOSE_TEST) run --rm test ./pytest.sh

test-down: ## Stop the test database and cache
	$(COMPOSE_TEST) down -v

lint: ## Check linting and formatting
	uv run ruff check .
	uv run ruff format --check .

format: ## Fix linting and formatting
	uv run ruff check --fix .
	uv run ruff format .

makemigrations: ## Create migrations; pass ARGS to target an app, e.g. make makemigrations ARGS=users
	@docker image inspect backend:test >/dev/null 2>&1 || $(MAKE) test-image
	$(COMPOSE_TEST) run --rm test python manage.py makemigrations $(ARGS)

migrate-check: ## Fail if models have changes without migrations
	@docker image inspect backend:test >/dev/null 2>&1 || $(MAKE) test-image
	$(COMPOSE_TEST) run --rm test python manage.py makemigrations --check --dry-run $(MIGRATION_APPS)
