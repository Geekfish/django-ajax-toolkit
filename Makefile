install:
    python setup.py develop
    pip install -r test_requirements

test:
    ./runtests.py

travis: install test

