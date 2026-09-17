CURENT_DIR=$(CURDIR)
TOML=$(CURENT_DIR)/pyproject.toml
VENV=.venv
PY_VENV=$(VENV)/bin/python
TARGET=installed
export UV_CACHE_DIR=/home/$(USER)/goinfre/uv_cache

all:$(TARGET) install uv_add_package

uv_add_package:
	@uv add pygame

$(TARGET): $(TOML)
	@touch $(TARGET)

$(TOML):
	@uv init

install:$(TARGET)
	@python -m venv $(VENV)
	@$(PY_VENV) -m pip install uv

sync:
	@uv sync

clean:
	uv cache clean

fclean:
	@rm -rf $(CURENT_DIR)/main.py
	@rm -rf $(CURENT_DIR)/pyproject.toml
	@rm -rf $(VENV)
	@rm -rf $(TARGET)
