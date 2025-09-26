.PHONY: formatters
formatters:
	black run.py prism
	isort run.py prism

.PHONY: code-check
code-check:
	black --check run.py prism
	isort --check run.py prism
	darglint run.py prism
	flake8 run.py prism
	pylint run.py prism
	mypy run.py prism

.PHONY: build
build:
	pyinstaller --onefile --windowed --name="Prism" run.py