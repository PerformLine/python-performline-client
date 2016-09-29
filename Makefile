.PHONY: clean test deps

all: clean build test

deps:
	pip install -r requirements.txt

build:
	pip install --editable .

test:
	@python test.py

clean:
	@find . -maxdepth 1 -type f -name "*.pyc" -delete
