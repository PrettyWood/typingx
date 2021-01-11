black = black typing_extend tests
isort = isort typing_extend tests

.PHONY: install
install:
	pip install poetry
	poetry install

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
	poetry run ${black} --diff --check
	poetry run ${isort} --check-only
	poetry run mypy typing_extend
