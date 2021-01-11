black = black typing_extend tests

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

.PHONY: lint
lint:
	poetry run ${black} --diff --check
