VENV=.venv
PY_VENV=$(VENV)/bin/python
INSTALLED = INSTALLED

.PHONY: all run run-folder install lint debug lint-strict clean fclean

all:install

$(INSTALLED):
	@touch $(INSTALLED)

run: install
	@$(PY_VENV) main.py $(ARGS)

run-folder: install
	@$(PY_VENV) main.py --folder $(ARGS)

install: $(INSTALLED)
	@python -m venv $(VENV)
	@$(PY_VENV) -m pip install uv
	@uv sync --python 3.11

debug:
	@$(PY_VENV) -m pdb main.py

lint:
	@$(PY_VENV) $(VENV)/bin/flake8 . --exclude=.venv && $(PY_VENV) $(VENV)/bin/mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --exclude .venv/

lint-strict:
	@$(PY_VENV) $(VENV)/bin/flake8 . --exclude=.venv && $(PY_VENV) $(VENV)/bin/mypy --install-types && \
		$(PY_VENV) $(VENV)/bin/mypy . --strict  --exclude .venv/

clean:
	@rm -rf __pycache* .mypy_cache .pytest_cache

fclean: clean
	@rm -rf $(VENV)
	@rm -rf $(INSTALLED)

re: fclean install