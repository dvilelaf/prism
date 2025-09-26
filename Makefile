.PHONY: formatters
formatters:
	black prism.py
	isort prism.py

.PHONY: code-check
code-check:
	black --check prism.py
	isort --check prism.py
	darglint prism.py
	flake8 prism.py
	pylint prism.py
	mypy prism.py

.PHONY: build
build:
	pyinstaller --onefile --windowed --name="prism" prism.py