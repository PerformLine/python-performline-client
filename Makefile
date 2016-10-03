.PHONY: clean test deps

all: venv test

venv:
	virtualenv --distribute venv

deps:
	pip install -I -r requirements.txt

test: deps
	flake8
	py.test performline/products/*/tests/*.py

clean:
	@find . -maxdepth 1 -type f -name "*.pyc" -delete
	rm -rf venv
