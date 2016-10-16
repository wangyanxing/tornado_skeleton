project := bootcamp
flake8 := flake8
TARGET ?= tests
pytest_args := -s --tb short --cov-config .coveragerc --cov $(project) $(TARGET)
pytest := $(clay_config) py.test $(pytest_args)

test_args := --cov-report term-missing --cov-report xml --junitxml junit.xml
ci_args := --cov-report=


CLAY_CONFIG ?= config/test.yaml
export CLAY_CONFIG
export CODECLIMATE_REPO_TOKEN=f49e0e055395186fb1eb773362e86306d8a043f4b383e8d4bec85780c2a2f61f

.DEFAULT_GOAL := test

.PHONY: bootstrap
bootstrap:
	pip install -U "setuptools>=19,<20"
	pip install -U "pip>=8"
	pip install -r requirements-tests.txt
	pip install -r requirements.txt
	python setup.py develop

.PHONY: bootstrap-db
bootstrap-db:
	CLAY_CONFIG=./config/base.yaml python ./scripts/bootstrap_db.py bootstrap

.PHONY: drop-db
drop-db:
	CLAY_CONFIG=./config/base.yaml python ./scripts/bootstrap_db.py drop

.PHONY: serve
serve:
	CLAY_CONFIG=./config/base.yaml bootcamp-web

.PHONY: clean
clean:
	@find $(project) "(" -name "*.pyc" -o -name "coverage.xml" -o -name "junit.xml" ")" -delete

.PHONY: test
test:
	@find $(project) "(" -name ".coverage.*" ")" -delete
	make lint
	python ./scripts/bootstrap_db.py bootstrap
	$(pytest) $(test_args)

.PHONY: report
report:
	codeclimate-test-reporter --file $(shell find . -name '*.coverage.*')

.PHONY: lint
lint:
	$(flake8) $(project) tests --config .flake8

.PHONY: shell
shell:
	ipython
