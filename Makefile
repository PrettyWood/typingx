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
