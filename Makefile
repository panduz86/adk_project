PYTHON ?= python3

.PHONY: help test run list-wines venv-setup clean-venv
VENV_DIR ?= .venv

help:
	@echo "Available targets:"
	@echo "  make test                 - run the pytest test suite (uses .venv/python if present, else system python3)"
	@echo "  make run                  - run the application (uses main.py)"
	@echo "  make run-debug            - run the application with debug logs"
	@echo "  make run-buy-agent-server - start the Buy Wine Agent on the port 8001"

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

run-buy-agent-server:
	$(PYTHON) agents/a2a_agents/run_buy_wine_a2a.py
