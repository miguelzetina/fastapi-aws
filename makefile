default: install test lint

test: lint test.all
test.cov: test.coverage

test.all:
	@pytest tests

lint:
	@pylint app tests src

format.check:
	@black . --check

format.fix:
	@black .

