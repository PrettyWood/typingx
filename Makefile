black = black typing_extend tests
isort = isort typing_extend tests

.PHONY: install
install:
	pip install poetry
	poetry install
	poetry run pre-commit install

.PHONY: test
test:
	poetry run pytest

.PHONY: test-all
test-all:
	tox -p all

.PHONY: format
format:
	poetry run ${black}
	poetry run ${isort}

.PHONY: lint
lint:
	poetry run flake8 typing_extend tests
	poetry run ${black} --diff --check
	poetry run ${isort} --check-only
	poetry run mypy typing_extend
