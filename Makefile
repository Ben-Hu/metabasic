.DEFAULT_GOAL := help

help: ## display this message
	@echo "usage: make [target]"
	@echo
	@echo "available targets:"
	@grep -h "##" $(MAKEFILE_LIST) | grep -v grep  | column -t -s '##'
	@echo

.PHONY: init
init: ## install pipenv and dev deps
	pip install poetry --upgrade --user
	poetry install

.PHONY: all
all: ## run code formatter, linting, and tests
all: format lint coverage

.PHONY: format
format: ## run code formatters
	poetry run isort -rc -sp .isort.cfg .
	poetry run black .

.PHONY: check_format
check_format: ## check for code formatter errors
	poetry run black . --check --diff

.PHONY: lint
lint: ## run mypy, flake8, and isort linter checks
	poetry run mypy --config-file=./mypy.ini .
	poetry run flake8 .
	poetry run isort -rc -sp .isort.cfg .

.PHONY: test
test: ## run test suite
	poetry run python -m pytest -v tests

.PHONY: coverage
coverage: ## run test suite and output coverage files
	poetry run pytest \
		--verbose \
		--cov-report term \
		--cov-report html:coverage/html \
		--cov-report xml:coverage/cover.xml \
		--cov-report annotate:coverage/annotate \
		--cov=metabasic \
		tests

.PHONY: build
build: ## generate distribution packages
	poetry build

.PHONY: tox
tox: ## Runs tox for testing against multiple python versions
	poetry run tox -p all $(TOX_ARGS)

.PHONY: docs
docs: ## generate html documentation for the package
	poetry run sphinx-apidoc metabasic --output-dir sphinx/source/metabasic/ --force --separate
	cd sphinx && poetry run make html
	cp -r sphinx/build/html/* docs/