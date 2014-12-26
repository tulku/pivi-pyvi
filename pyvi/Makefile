all: install

install:
	python setup.py install

test: install
	python tests/UnitTests.py

coverage: install
	coverage run tests/UnitTests.py
	coverage report -m

clean:
	python-coverage erase
	python setup.py clean
