init:
	pip install -r requirements.txt

test:
	pytest -vvv --log-cli-level=INFO tests

.PHONY: init test