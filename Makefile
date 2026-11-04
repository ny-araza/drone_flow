VENV=.venv
PY_VENV=$(VENV)/bin/python
INSTALLED = .installed


.PHONY: all install_package run run-folder install lint lint-strict clean fclean

all:install

run: $(INSTALLED)
	@$(PY_VENV) main.py $(ARGS)

run-folder: $(INSTALLED)
	@$(PY_VENV) main.py --folder $(ARGS)

install:
	@python -m venv $(VENV)
	@$(PY_VENV) -m pip install uv
	@uv sync --python 3.11
	@touch $(INSTALLED)

debug:
	@$(PY_VENV) -m pdb main.py

lint: $(INSTALLED)
	@$(PY_VENV) $(VENV)/bin/flake8 . --exclude=.venv && $(PY_VENV) $(VENV)/bin/mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --exclude .venv/

lint-strict: $(INSTALLED)
	@$(PY_VENV) $(VENV)/bin/flake8 . --exclude=.venv && $(PY_VENV) $(VENV)/bin/mypy --install-types && \
		$(PY_VENV) $(VENV)/bin/mypy . --strict  --exclude .venv/

clean:
	@rm -rf __pycache* .mypy_cache

fclean: clean
	@rm -rf $(VENV)
	@rm -rf $(INSTALLED)

re: fclean install