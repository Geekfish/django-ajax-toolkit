.PHONY: test travis
install:
	python setup.py develop
	pip install -r test_requirements.txt

test:
	./runtests.py

travis: install test

