.PHONY: clean test deps

all: venv library-prefix test

deps:
	pip install -I -r requirements.txt

test-deps:
	pip install -I -r test-requirements.txt

docs-deps:
	pip install -I -r doc-requirements.txt

test:
	test "${TRAVIS_PYTHON_VERSION}" == "2.6" || flake8
	tox

library-prefix:
	@bash contrib/apply-license-prefix

docs-clean:
	rm -rf doc/build/html/*
	rm -rf doc/build/doctrees/*

clean-build:
	test -d build && rm -rf build || true
	test -d dist && rm -rf dist || true
	test -d performline.egg-info && rm -rf performline.egg-info || true

clean: clean-build docs-clean
	@find . -maxdepth 1 -type f -name "*.pyc" -delete
	rm -rf venv

docs-build: docs-clean
	@cd doc && make html

docs: doc-deps docs-build

package-build: clean-build
	python setup.py sdist bdist_wheel

package-sign:
	cd dist && gpg \
		--detach-sign \
		--armor \
		--passphrase-file ../sign.key \
		--batch \
		--yes *.tar.gz

package-push:
	twine upload --skip-existing dist/*

package-push-test:
	twine upload --skip-existing -r pypitest dist/*

package: deps library-prefix package-build package-sign package-push

package-test: deps library-prefix package-build package-sign package-push-test


