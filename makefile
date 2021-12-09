init:
	pip install -r requirements.txt

test:
	pytest -vvv --cov=sudoku --log-cli-level=INFO tests

.PHONY: init test