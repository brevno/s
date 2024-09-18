APP_NAME=main.py
VENV_DIR=venv
PYTHON=python3
PIP=$(VENV_DIR)/bin/pip
ALEMBIC=$(VENV_DIR)/bin/alembic

.PHONY: all install run-server clean migrations install-ui run-ui test

all: install install-ui run

run: run-server run-ui

install:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

run-server:
	@echo "Running FastAPI application..."
	venv/bin/python -m main &
	@server_pid=$!

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
	rm -rf ui/node_modules

migrations:
	@echo "Creating a new migration..."
	$(ALEMBIC) revision --autogenerate -m "New migration"
	@echo "Applying the migration..."
	$(ALEMBIC) upgrade head

install-ui:
	@echo "Installing UI dependencies..."
	cd ui && npm install

run-ui:
	@echo "Running UI..."
	cd ui && npm start &
	@ui_pid=$!

kill:
	@echo "Killing the server..."
	fuser -k 8000/tcp
	@echo "Killing the UI..."
	fuser -k 3000/tcp

test:
	@echo "Running tests..."
	PYTHONPATH=$(shell pwd) $(VENV_DIR)/bin/pytest