VENV=.venv
PY_VENV=$(VENV)/bin/python
INSTALLED = INSTALLED

.PHONY: all run run-folder install lint debug lint-strict clean fclean

all:install

run:
	@uv run python main.py $(ARGS)

run-folder:
	@uv run python main.py --folder $(ARGS)

install:
	@python -m venv $(VENV)
	@$(PY_VENV) -m pip install uv
	@uv sync --python 3.11

debug:
	@uv run python -m pdb main.py

lint:
	@uv run flake8 . --exclude=.venv && uv run mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --exclude .venv/

lint-strict:
	@uv run flake8 . --exclude=.venv && uv run mypy --install-types && \
		uv run mypy . --strict  --exclude .venv/

clean:
	@rm -rf __pycache* .mypy_cache .pytest_cache

fclean: clean
	@rm -rf $(VENV)
	@rm -rf $(INSTALLED)

re: fclean install