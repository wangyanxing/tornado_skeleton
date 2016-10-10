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
