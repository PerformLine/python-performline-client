.PHONY: clean just-test test deps

all: venv library-prefix test

venv:
	virtualenv --distribute venv

deps:
	pip install -I -r requirements.txt

test-deps:
	pip install -I -r test-requirements.txt

just-test:
	test "${TRAVIS_PYTHON_VERSION}" == "2.6" || flake8
	py.test performline/products/*/tests/*.py

test: test-deps just-test

library-prefix:
	@bash contrib/apply-license-prefix

clean-build:
	test -d build && rm -rf build || true
	test -d dist && rm -rf dist || true
	test -d performline.egg-info && rm -rf performline.egg-info || true

clean: clean-build
	@find . -maxdepth 1 -type f -name "*.pyc" -delete
	rm -rf venv

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


