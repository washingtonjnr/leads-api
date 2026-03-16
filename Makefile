.PHONY: help test test-verbose test-cov test-specific clean install-test lint format

help:
	@echo "CE-API-II - Available commands:"
	@echo ""
	@echo "Installation:"
	@echo "  make install-test       Install test dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test               Run all tests"
	@echo "  make test-verbose       Run all tests with verbose output"
	@echo "  make test-cov           Run tests with coverage report"
	@echo "  make test-specific      Run specific test (use TEST=path/file.py)"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint               Run code linting (if configured)"
	@echo "  make format             Format code (if configured)"
	@echo ""
	@echo "Development:"
	@echo "  make run                Run the application"
	@echo "  make clean              Clean cache and temporary files"
	@echo ""

install-test:
	pip install -r requirements/test.txt

test:
	pytest tests/ -q

test-verbose:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

test-specific:
	pytest $(TEST) -v

test-schemas:
	pytest tests/test_schemas.py -v

test-models:
	pytest tests/test_models.py -v

test-services:
	pytest tests/test_services.py -v

test-repositories:
	pytest tests/test_repositories.py -v

test-controllers:
	pytest tests/test_controllers.py -v

test-utils:
	pytest tests/test_utils.py -v

test-async:
	pytest tests/ -v -m asyncio

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run:
	python run.py

lint:
	@echo "Linting is not configured. Consider adding flake8, pylint, or similar."

format:
	@echo "Code formatting is not configured. Consider adding black or similar."

.DEFAULT_GOAL := help
