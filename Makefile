VENV=.venv
PY_VENV=$(VENV)/bin/python

.PHONY: all install_package run run-folder install lint lint-strict clean fclean

all:install

run:
	@$(PY_VENV) main.py $(ARGS)

run-folder:
	@$(PY_VENV) main.py --folder $(ARGS)

install:
	@python -m venv $(VENV)
	@$(PY_VENV) -m pip install -r requirements.txt

lint:
	@$(PY_VENV) $(VENV)/bin/flake8 . --exclude=.venv && $(PY_VENV) $(VENV)/bin/mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --exclude .venv/

lint-strict:
	@$(PY_VENV) $(VENV)/bin/flake8 . --exclude=.venv && mypy --install-types && \
		$(PY_VENV) $(VENV)/bin/mypy . --strict  --exclude .venv/

clean:
	@rm -rf __pycache* .mypy_cache

fclean: clean
	@rm -rf $(VENV)

re: fclean install