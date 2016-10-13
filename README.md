[![Build Status](https://travis-ci.org/cjlm007/tornado_skeleton.svg?branch=master)](https://travis-ci.org/cjlm007/tornado_skeleton) [![Code Climate](https://codeclimate.com/github/cjlm007/tornado_skeleton/badges/gpa.svg)](https://codeclimate.com/github/cjlm007/tornado_skeleton) [![Test Coverage](https://codeclimate.com/github/cjlm007/tornado_skeleton/badges/coverage.svg)](https://codeclimate.com/github/cjlm007/tornado_skeleton/coverage)

## Prerequisites

* Install pip:
https://pip.pypa.io/en/stable/installing

* Install postgres  

`brew install postgres`

* Others

`pip install ipython`

## Install

```
virtualenv env
source env/bin/activate
make bootstrap
make bootstrap-db
```

## Run

```
source env/bin/activate
make serve
http://localhost:18888/
```

## Test

```
make test
```
