.PHONY: clean test deps

all: venv clean test

venv:
	virtualenv --distribute venv

deps:
	pip install -r requirements.txt

test:
	flake8 || make deps
	py.test performline/products/*/tests/*.py

clean:
	@find . -maxdepth 1 -type f -name "*.pyc" -delete
