init:
	pip install -r requirements.txt

test:
	pytest -vvv --cov=sudoku --log-cli-level=INFO tests

covRep:
	coverage report -m

.PHONY: init test