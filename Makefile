CURENT_DIR=$(CURDIR)
TOML=$(CURENT_DIR)/pyproject.toml
VENV=.venv
PY_VENV=$(VENV)/bin/python
export UV_CACHE_DIR=/home/$(USER)/goinfre/uv_cache

all:$(TARGET) install install_package run

install_package:
	@$(PY_VENV) -m pip install -r requirements.txt

run:
	@$(PY_VENV) main.py $(ARGS)

run-folder:
	@$(PY_VENV) main.py --folder $(ARGS)

install:
	@python -m venv $(VENV)

lint:
	@$(PY_VENV) -m flake8 . --exclude=.venv && mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --exclude .venv/

lint-strict:
	@$(PY_VENV) -m flake8 . --exclude=.venv && mypy --install-types && \
		mypy . --strict  --exclude .venv/

clean:
	@rm -rf __pycache*

fclean: clean
	@rm -rf $(VENV)
