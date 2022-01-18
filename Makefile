.DEFAULT_GOAL := all
black = black typingx tests
isort = isort typingx tests

.PHONY: install
install:
	pip install -U pip
	pip install poetry
	poetry install
	poetry run pre-commit install

.PHONY: test
test:
	poetry run pytest

.PHONY: format
format:
	poetry run ${black}
	poetry run ${isort}

.PHONY: lint
lint:
	poetry run flake8 typingx tests
	poetry run ${black} --diff --check
	poetry run ${isort} --check-only
	poetry run mypy typingx

.PHONY: all
all: lint test
