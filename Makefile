CURENT_DIR=$(CURDIR)
TOML=$(CURENT_DIR)/pyproject.toml
VENV=.venv
PY_VENV=$(VENV)/bin/python
TARGET=installed
export UV_CACHE_DIR=/home/$(USER)/goinfre/uv_cache

all:$(TARGET) install uv_add_package

uv_add_package:
	@uv add pygame colorama flake8 mypy

$(TARGET): $(TOML)
	@touch $(TARGET)

$(TOML):
	@uv init

run:
	@uv run python -m src maps

install:$(TARGET)
	@python -m venv $(VENV)
	@$(PY_VENV) -m pip install uv

lint:
	@$(PY_VENV) -m flake8 . --exclude=.venv && mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --exclude .venv/

lint-strict:
	@$(PY_VENV) -m flake8 . --exclude=.venv && mypy . --strict --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --exclude .venv/

sync:
	@uv sync

clean:
	uv cache clean

fclean:
	@rm -rf $(CURENT_DIR)/main.py
	@rm -rf $(CURENT_DIR)/pyproject.toml
	@rm -rf $(VENV)
	@rm -rf $(TARGET)
