.PHONY: clean test deps

all: env deps library-prefix test

env:
	virtualenv --distribute env

deps:
	./env/bin/pip install -I -r requirements.txt
	./env/bin/pip install -I -r test-requirements.txt
	./env/bin/pip install -I -r doc-requirements.txt

test:
	test "${TRAVIS_PYTHON_VERSION}" == "2.6" || ./env/bin/flake8 -v
	./env/bin/tox

library-prefix:
	@bash contrib/apply-license-prefix

docs-clean:
	-rm -rf doc/build/html/*
	-rm -rf doc/build/doctrees/*

clean-build:
	-rm -rf build dist *.egg-info

clean: clean-build docs-clean
	-rm -rf env
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


