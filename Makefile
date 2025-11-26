PYTHON ?= python3

.PHONY: help test run list-wines venv-setup clean-venv
VENV_DIR ?= .venv

help:
	@echo "Available targets:"
	@echo "  make test       - run the pytest test suite (uses .venv/python if present, else system python3)"
	@echo "  make run        - run the application (uses main.py)"

test:
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_DIR)/bin/python -m pytest -q; \
	else \
		$(PYTHON) -m pytest -q; \
	fi

run:
	$(PYTHON) main.py

run-debug:
	$(PYTHON) main.py --debug
