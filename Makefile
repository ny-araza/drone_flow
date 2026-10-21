VENV=.venv
PY_VENV=$(VENV)/bin/python

.PHONY: all install_package run run-folder install lint lint-strict clean fclean

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
	@rm -rf $(VENV) .mypy_cache maps

re: fclean all