PYTHON ?= python3
VENV ?= .venv
PYTHON_BIN := $(VENV)/bin/python
PIP_BIN := $(VENV)/bin/pip

.PHONY: install test lint run train evaluate export

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP_BIN) install --upgrade pip
	$(PIP_BIN) install -r requirements.txt

test:
	$(PYTHON_BIN) -m pytest -q

lint:
	$(PYTHON_BIN) -m ruff check .

run:
	$(PYTHON_BIN) -m uvicorn api.main:app --reload

train:
	$(PYTHON_BIN) scripts/train.py

evaluate:
	$(PYTHON_BIN) scripts/evaluate.py

export:
	$(PYTHON_BIN) scripts/export.py
