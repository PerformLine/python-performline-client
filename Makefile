.PHONY: clean test deps

all: clean test

deps:
	pip install -r requirements.txt

test:
	flake8
	py.test performline/products/*/tests/*.py

clean:
	@find . -maxdepth 1 -type f -name "*.pyc" -delete
