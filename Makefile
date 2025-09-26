.PHONY: formatters
formatters:
	black run.py triton
	isort run.py triton

.PHONY: code-check
code-check:
	black --check run.py triton
	isort --check run.py triton
	darglint run.py triton
	flake8 run.py triton
	pylint run.py triton
	mypy run.py triton