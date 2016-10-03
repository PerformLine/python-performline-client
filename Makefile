.PHONY: clean just-test test deps

all: venv test

venv:
	virtualenv --distribute venv

deps:
	pip install -I -r requirements.txt

just-test:
	flake8
	py.test performline/products/*/tests/*.py

test: deps just-test

clean:
	@find . -maxdepth 1 -type f -name "*.pyc" -delete
	rm -rf venv
