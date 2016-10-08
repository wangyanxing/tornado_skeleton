project := bootcamp
flake8 := flake8
TARGET ?= tests
pytest_args := -s --tb short --cov-config .coveragerc --cov $(project) $(TARGET)
pytest := $(clay_config) py.test $(pytest_args)

html_report := --cov-report html
test_args := --cov-report term-missing --cov-report xml --junitxml junit.xml


CLAY_CONFIG ?= config/test.yaml
export CLAY_CONFIG

.DEFAULT_GOAL := test

.PHONY: bootstrap
bootstrap:
	pip install -U "setuptools>=19,<20"
	pip install -U "pip>=7,<8"
	pip install -r requirements-tests.txt
	pip install -r requirements.txt
	python setup.py develop

.PHONY: bootstrap-db
bootstrap-db:
	python ./scripts/bootstrap_db.py bootstrap

.PHONY: drop-db
drop-db:
	python ./scripts/bootstrap_db.py drop

.PHONY: serve
serve:
	bootcamp-web

.PHONY: clean
clean:
	@find $(project) "(" -name "*.pyc" -o -name "coverage.xml" -o -name "junit.xml" ")" -delete

.PHONY: test
test: clean
	$(pytest) $(test_args)

.PHONY: lint
lint:
	$(flake8) $(project) tests --config .flake8

.PHONY: shell
shell:
	ipython
