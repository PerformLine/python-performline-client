.PHONY: clean test deps

all: env deps performline/embedded/stdlib library-prefix test

env:
	which virtualenv || pip install virtualenv
	virtualenv env

deps:
	./env/bin/pip install -I -r requirements.txt
	./env/bin/pip install -I -r test-requirements.txt
	./env/bin/pip install -I -r doc-requirements.txt

performline/embedded/stdlib:
	-mkdir -p performline/embedded/stdlib
	touch performline/embedded/__init__.py
	rsync \
		--archive \
		--verbose \
		--delete-after \
		--filter='H *.pyc' \
		--filter='H __pycache__/' \
		--filter='H *_test.py' \
		--filter='+ /__init__.py' \
		--filter='+ /utils/' \
		--filter='+ /utils/*.py' \
		--filter='+ /clients/' \
		--filter='+ /clients/__init__.py' \
		--filter='+ /clients/rest/' \
		--filter='+ /clients/rest/**' \
		--filter='H *' \
		../python-performline-stdlib/performline/ ./performline/embedded/stdlib/

test: clean-cache
	test "${TRAVIS_PYTHON_VERSION}" == "2.6" || ./env/bin/flake8
	./env/bin/py.test -v -o norecursedirs='.cache .eggs .git env .tox'

library-prefix:
	@bash contrib/apply-license-prefix

docs-clean:
	-rm -rf doc/build/html/*
	-rm -rf doc/build/doctrees/*

clean-build:
	-rm -rf build dist *.egg-info

clean-cache:
	-rm -rf build dist
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

clean: clean-build docs-clean clean-cache
	-rm -rf env

docs-build: docs-clean
	@cd doc && make html

docs: deps docs-build

package-build:
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
	./env/bin/twine upload --config-file $(or $$PYPIRC,$$PYPIRC,~/.pypirc) --skip-existing dist/*

package-push-test:
	./env/bin/twine upload --config-file $(or $$PYPIRC,$$PYPIRC,~/.pypirc) --skip-existing -r pypitest dist/*

package: package-build package-sign package-push

package-test: deps library-prefix test package-build package-sign package-push-test clean-cache

shell:
	test -x ./env/bin/ipython || ./env/bin/pip install ipython
	./env/bin/ipython
