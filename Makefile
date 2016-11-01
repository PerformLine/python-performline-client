.PHONY: clean test deps

all: env deps embed-stdlib library-prefix test

env:
	virtualenv --distribute env

deps:
	./env/bin/pip install -q -I -r requirements.txt
	./env/bin/pip install -q -I -r test-requirements.txt
	./env/bin/pip install -q -I -r doc-requirements.txt

embed-stdlib:
	-mkdir -p performline/embedded/stdlib
	touch performline/embedded/__init__.py
	rsync \
		--archive \
		--verbose \
		--delete-after \
		--filter='- *.pyc' \
		--filter='- __pycache__/' \
		--filter='+ /__init__.py' \
		--filter='+ /utils/' \
		--filter='+ /utils/*.py' \
		--filter='+ /clients/' \
		--filter='+ /clients/__init__.py' \
		--filter='+ /clients/rest/' \
		--filter='+ /clients/rest/**' \
		--filter='- *' \
		../python-performline-stdlib/performline/ ./performline/embedded/stdlib/

test:
	test "${TRAVIS_PYTHON_VERSION}" == "2.6" || ./env/bin/flake8
	./env/bin/py.test -v -o norecursedirs='.cache .eggs .git env .tox'

library-prefix:
	@bash contrib/apply-license-prefix

docs-clean:
	-rm -rf doc/build/html/*
	-rm -rf doc/build/doctrees/*

clean-build:
	-rm -rf build dist *.egg-info

clean: clean-build docs-clean
	-rm -rf env
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete
	-@find . -maxdepth 1 -type f -name "*.pyc" -delete

docs-build: docs-clean
	@cd doc && make html

docs: deps docs-build

package-build: clean-build
	./env/bin/python setup.py sdist bdist_wheel

package-sign:
	cd dist && gpg \
		--local-user 5B2B38E1 \
		--detach-sign \
		--armor \
		--passphrase-file ../sign.key \
		--batch \
		--yes *.tar.gz

package-push:
	./env/bin/twine upload --skip-existing dist/*

package-push-test:
	./env/bin/twine upload --skip-existing -r pypitest dist/*

package: deps library-prefix test package-build package-sign package-push

package-test: deps library-prefix test package-build package-sign package-push-test


